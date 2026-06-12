# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """Extend sale.order with POS counter-payment functionality.

    New additions
    -------------
    * ``pos_session_id``  – the POS session that will receive the counter order
      (pre-filled with the open session owned by the current user; editable in
      the "Other Info" tab).
    * State ``paid_at_counter`` – behaves like ``cancel``: the order is locked,
      no further edits are possible, and the standard action buttons are hidden.
    * ``pay_at_counter_visible`` – computed flag that drives button/state-badge
      visibility.
    * ``action_pay_at_counter`` – opens the payment wizard.
    """

    _inherit = 'sale.order'

    # ------------------------------------------------------------------ #
    #  New selection state injected into the existing state field          #
    # ------------------------------------------------------------------ #
    state = fields.Selection(
        selection_add=[('paid_at_counter', 'Paid at Counter')],
        ondelete={'paid_at_counter': 'set default'},
    )

    # ------------------------------------------------------------------ #
    #  POS session field (Other Info tab)                                  #
    # ------------------------------------------------------------------ #
    pos_session_id = fields.Many2one(
        comodel_name='pos.session',
        string='POS Session',
        domain=[('state', '=', 'opened')],
        help='The open POS session that will receive this order when '
             '"Pay at the Counter" is confirmed. Defaults to the session '
             'currently opened by the responsible user.',
        copy=False,
        tracking=True,
    )

    # ------------------------------------------------------------------ #
    #  Visibility helper (used in button attrs & status bar)               #
    # ------------------------------------------------------------------ #
    pay_at_counter_visible = fields.Boolean(
        string='Pay at Counter Visible',
        compute='_compute_pay_at_counter_visible',
        store=False,
    )

    # ------------------------------------------------------------------ #
    #  Related POS order (for traceability)                                #
    # ------------------------------------------------------------------ #
    pos_order_id = fields.Many2one(
        comodel_name='pos.order',
        string='POS Order',
        readonly=True,
        copy=False,
    )

    # ------------------------------------------------------------------ #
    #  Compute helpers                                                     #
    # ------------------------------------------------------------------ #
    @api.depends('state')
    def _compute_pay_at_counter_visible(self):
        for order in self:
            order.pay_at_counter_visible = order.state == 'sale'

    # ------------------------------------------------------------------ #
    #  Default POS session (triggered when the responsible user changes)   #
    # ------------------------------------------------------------------ #
    @api.onchange('user_id')
    def _onchange_user_id_pos_session(self):
        """Pre-fill pos_session_id with the open session owned by user_id."""
        self._set_default_pos_session()

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            order._set_default_pos_session()
        return orders

    def _set_default_pos_session(self):
        """Assign the open POS session belonging to self.user_id, if any."""
        for order in self:
            session = self.env['pos.session'].search([
                ('state', '=', 'opened'),
                ('user_id', '=', order.user_id.id),
            ], limit=1)
            order.pos_session_id = session or False

    # ------------------------------------------------------------------ #
    #  Button action                                                       #
    # ------------------------------------------------------------------ #
    def action_pay_at_counter(self):
        """Open the POS counter-payment wizard for this sale order."""
        self.ensure_one()

        if self.state != 'sale':
            raise UserError(_('Only confirmed sale orders can be paid at the counter.'))

        if not self.pos_session_id:
            raise UserError(_(
                'No open POS session is set for this order.\n'
                'Please assign an open POS session in the "Other Info" tab.'
            ))

        if not self.order_line:
            raise UserError(_('There are no order lines to transfer to the POS.'))

        # Build default wizard payment lines from the session's payment methods
        payment_method_lines = []
        for pm in self.pos_session_id.payment_method_ids:
            payment_method_lines.append((0, 0, {
                'payment_method_id': pm.id,
                'amount': 0.0,
            }))

        wizard = self.env['sale.pos.payment.wizard'].create({
            'sale_order_id': self.id,
            'pos_session_id': self.pos_session_id.id,
            'payment_line_ids': payment_method_lines,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': _('Pay at the Counter'),
            'res_model': 'sale.pos.payment.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    # ------------------------------------------------------------------ #
    #  POS order creation (called from wizard)                             #
    # ------------------------------------------------------------------ #
    def _create_pos_order_from_sale(self, wizard_rec):
        """Create and validate a POS order from *self* using wizard data.

        Parameters
        ----------
        wizard_rec : sale.pos.payment.wizard
            The confirmed payment wizard record.

        Returns
        -------
        pos.order
            The newly created (and validated) POS order.
        """
        self.ensure_one()
        PosOrder = self.env['pos.order']
        session = self.pos_session_id

        # ---- Build order lines ----------------------------------------
        pos_lines = []
        for line in self.order_line:
            if line.display_type:
                # Skip section/note lines — POS doesn't support them
                continue
            # pos.order.line uses 'tax_ids' in Odoo 17
            pos_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'full_product_name': line.name,
                'qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_ids': [(6, 0, line.tax_id.ids)],
                'price_subtotal': line.price_subtotal,
                'price_subtotal_incl': line.price_total,
            }))

        if not pos_lines:
            raise UserError(_('No transferable product lines found on the sale order.'))

        # ---- Compute tax total ----------------------------------------
        amount_tax = sum(
            line.price_total - line.price_subtotal
            for line in self.order_line
            if not line.display_type
        )

        # ---- Create the POS order (without payments first) -----------
        pos_order_vals = {
            'session_id': session.id,
            'partner_id': self.partner_id.id or False,
            'fiscal_position_id': self.fiscal_position_id.id or False,
            'lines': pos_lines,
            'amount_total': wizard_rec.total_amount,
            'amount_paid': wizard_rec.paid_amount,
            'amount_return': max(0.0, wizard_rec.paid_amount - wizard_rec.total_amount),
            'amount_tax': amount_tax,
        }
        # Link back to the source sale order if the field exists
        # (e.g. when sale_management bridge is installed or via custom field)
        if 'sale_order_id' in PosOrder._fields:
            pos_order_vals['sale_order_id'] = self.id

        pos_order = PosOrder.create(pos_order_vals)

        # ---- Create payment records linked to the POS order ----------
        PosPayment = self.env['pos.payment']
        for wline in wizard_rec.payment_line_ids.filtered(lambda l: l.amount > 0):
            PosPayment.create({
                'pos_order_id': pos_order.id,
                'payment_method_id': wline.payment_method_id.id,
                'amount': wline.amount,
                'payment_date': fields.Datetime.now(),
                'session_id': session.id,
            })

        # Invalidate cache so amount_paid recomputes from the new payment records
        pos_order.invalidate_recordset(['amount_paid'])

        # ---- Validate the POS order ----------------------------------
        pos_order.action_pos_order_paid()

        # ---- Transition the sale order --------------------------------
        self.write({
            'state': 'paid_at_counter',
            'pos_order_id': pos_order.id,
        })

        # Log traceability message in sale order chatter
        self.message_post(
            body=_(
                'Order paid at the counter. POS Order: <a href="#" '
                'data-oe-model="pos.order" data-oe-id="%(pos_id)s">%(pos_name)s</a>',
                pos_id=pos_order.id,
                pos_name=pos_order.name,
            )
        )

        return pos_order
