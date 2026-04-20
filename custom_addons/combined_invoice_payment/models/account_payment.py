# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    combined_invoice_payment_id = fields.Many2many('account.move')

    def action_post(self):
        """ pay invoice from payment model """
        res = super().action_post()

        invoice_ids = self.combined_invoice_payment_id.ids

        if self.combined_invoice_payment_id:
            return {
                'name': 'Register Payment',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment.register',
                'view_mode': 'form',
                'view_id': self.env.ref('account.view_account_payment_register_form').id,
                'target': 'new',
                'context': {
                    'active_model': 'account.move',
                    'active_ids': invoice_ids,
                    'default_amount': self.combined_invoice_payment_id.custom_payment_amount
                },
            }
        return res