# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('paid_at_counter', 'Paid at Counter')],
        ondelete={'paid_at_counter': 'set default'},
    )

    pos_session_id = fields.Many2one('pos.session',string='POS Session',domain=[('state', '=', 'opened')],)
    pay_at_counter_visible = fields.Boolean(string='pay counter',compute='_compute_pay_at_counter_visible')
    pos_order_id = fields.Many2one('pos.order',string='POS Order',copy=False,)

    @api.depends('state')
    def _compute_pay_at_counter_visible(self):
        for order in self:
            order.pay_at_counter_visible = order.state == 'sale'

    @api.onchange('user_id')
    def _onchange_user_id_pos_session(self):
        self._set_default_pos_session()

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            order._set_default_pos_session()
        return orders

    def _set_default_pos_session(self):
        for order in self:
            session = self.env['pos.session'].search([
                ('state', '=', 'opened'),
                ('user_id', '=', order.user_id.id),
            ], limit=1)
            order.pos_session_id = session or False

    def action_pay_at_counter(self):
        self.ensure_one()

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

    def create_pos_order_from_sale(self, wizard_rec):

        self.ensure_one()
        PosOrder = self.env['pos.order']
        session = self.pos_session_id

        pos_lines = []
        for line in self.order_line:
            if line.display_type:
                continuexpath
            pos_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'full_product_name': line.name,
                'qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_ids': [(6, 0, line.tax_ids.ids)],
                'price_subtotal': line.price_subtotal,
                'price_subtotal_incl': line.price_total,
            }))

        amount_tax = sum(
            line.price_total - line.price_subtotal
            for line in self.order_line
            if not line.display_type
        )

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
        if 'sale_order_id' in PosOrder._fields:
            pos_order_vals['sale_order_id'] = self.id

        pos_order = PosOrder.create(pos_order_vals)

        pos_payment = self.env['pos.payment']
        for wline in wizard_rec.payment_line_ids.filtered(lambda l: l.amount > 0):
            pos_payment.create({
                'pos_order_id': pos_order.id,
                'payment_method_id': wline.payment_method_id.id,
                'amount': wline.amount,
                'payment_date': fields.Datetime.now(),
                'session_id': session.id,
            })

        pos_order.invalidate_recordset(['amount_paid'])

        pos_order.action_pos_order_paid()
        self.write({
            'state': 'paid_at_counter',
            'pos_order_id': pos_order.id,
        })

        return pos_order

