# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """ Check the customer reached the credit limit"""
        invoice = self.env['account.move'].search([
            ('payment_state', '!=', 'paid'),
            ('move_type', '=', 'out_invoice'),
            ('partner_id', '=', self.partner_id),
        ]).mapped('amount_total')

        total_outstanding = sum(invoice)

        if total_outstanding > self.partner_id.credit_limit:
            raise UserError("Your outstanding credit reached")

        return super().action_confirm()