# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


class SalePosPaymentWizard(models.TransientModel):
    """Wizard: collect POS payments for a sale order before creating a POS order.

    Fields
    ------
    sale_order_id      – the source sale order (readonly, context-set)
    pos_session_id     – the target POS session (readonly, from sale order)
    payment_line_ids   – one2many: one line per payment method of the session
    total_amount       – computed total of the sale order (amount_total)
    paid_amount        – computed sum of payment lines
    remaining_amount   – computed total_amount - paid_amount
    """

    _name = 'sale.pos.payment.wizard'
    _description = 'Pay Sale Order at Counter'

    # ------------------------------------------------------------------ #
    #  Header fields                                                       #
    # ------------------------------------------------------------------ #
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        required=True,
        readonly=True,
    )

    pos_session_id = fields.Many2one(
        comodel_name='pos.session',
        string='POS Session',
        required=True,
        readonly=True,
    )

    currency_id = fields.Many2one(
        related='sale_order_id.currency_id',
        readonly=True,
    )

    # ------------------------------------------------------------------ #
    #  Payment lines                                                       #
    # ------------------------------------------------------------------ #
    payment_line_ids = fields.One2many(
        comodel_name='sale.pos.payment.wizard.line',
        inverse_name='wizard_id',
        string='Payments',
    )

    # ------------------------------------------------------------------ #
    #  Amount totals                                                       #
    # ------------------------------------------------------------------ #
    total_amount = fields.Monetary(
        string='Total Amount',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
    )

    paid_amount = fields.Monetary(
        string='Paid Amount',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
    )

    remaining_amount = fields.Monetary(
        string='Remaining Amount',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
    )

    # ------------------------------------------------------------------ #
    #  Compute                                                             #
    # ------------------------------------------------------------------ #
    @api.depends('sale_order_id.amount_total', 'payment_line_ids.amount')
    def _compute_amounts(self):
        for wizard in self:
            total = wizard.sale_order_id.amount_total or 0.0
            paid = sum(wizard.payment_line_ids.mapped('amount'))
            wizard.total_amount = total
            wizard.paid_amount = paid
            wizard.remaining_amount = total - paid

    def action_confirm_payment(self):
        """Validate amounts and delegate POS order creation to the sale order."""
        self.ensure_one()

        if not self.payment_line_ids.filtered(lambda l: l.amount > 0):
            raise UserError(_('Please enter at least one payment amount.'))

        precision = self.env['decimal.precision'].precision_get('Account')
        if float_compare(self.remaining_amount, 0.0, precision_digits=precision) > 0:
            raise UserError(_(
                'The paid amount (%(paid)s) is less than the total due (%(total)s).\n'
                'Remaining: %(remaining)s',
                paid=self.paid_amount,
                total=self.total_amount,
                remaining=self.remaining_amount,
            ))

        pos_order = self.sale_order_id._create_pos_order_from_sale(self)

        # Close wizard and open the created POS order for traceability
        return {
            'type': 'ir.actions.act_window',
            'name': _('POS Order'),
            'res_model': 'pos.order',
            'res_id': pos_order.id,
            'view_mode': 'form',
            'target': 'current',
        }


class SalePosPaymentWizardLine(models.TransientModel):
    """One payment method entry inside the counter-payment wizard."""

    _name = 'sale.pos.payment.wizard.line'
    _description = 'Counter Payment Line'

    wizard_id = fields.Many2one(
        comodel_name='sale.pos.payment.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade',
    )

    payment_method_id = fields.Many2one(
        comodel_name='pos.payment.method',
        string='Payment Method',
        required=True,
    )

    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
        default=0.0,
    )

    currency_id = fields.Many2one(
        related='wizard_id.currency_id',
        readonly=True,
    )
