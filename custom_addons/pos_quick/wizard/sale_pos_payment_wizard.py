# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SalePosPaymentWizard(models.TransientModel):
    _name = 'sale.pos.payment.wizard'
    _description = 'Pay Sale Order at Counter'

    sale_order_id = fields.Many2one('sale.order',string='Sale Order',)
    pos_session_id = fields.Many2one('pos.session',string='POS Session',)
    currency_id = fields.Many2one(related='sale_order_id.currency_id',)
    payment_line_ids = fields.One2many('sale.pos.payment.wizard.line',inverse_name='wizard_id',string='Payments',)
    total_amount = fields.Monetary(string='Total Amount',compute='_compute_amounts',store=True,)
    paid_amount = fields.Monetary(string='Paid Amount',compute='_compute_amounts',store=True,)
    remaining_amount = fields.Monetary(string='Remaining Amount',compute='_compute_amounts',store=True,)

    @api.depends('sale_order_id.amount_total', 'payment_line_ids.amount')
    def _compute_amounts(self):
        for wizard in self:
            total = wizard.sale_order_id.amount_total or 0.0
            paid = sum(wizard.payment_line_ids.mapped('amount'))
            wizard.total_amount = total
            wizard.paid_amount = paid
            wizard.remaining_amount = total - paid

    def action_confirm_payment(self):
        self.ensure_one()

        pos_order = self.sale_order_id._create_pos_order_from_sale(self)
        return {
            'type': 'ir.actions.act_window',
            'name': _('POS Order'),
            'res_model': 'pos.order',
            'res_id': pos_order.id,
            'view_mode': 'form',
            'target': 'current',
        }
