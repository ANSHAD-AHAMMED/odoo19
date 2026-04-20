# -*- coding: utf-8 -*-
from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    checkout_id = fields.Many2one('library.checkout', string="Checkout")

    def write(self, vals):
        """ Change the status of the checkout """
        res = super().write(vals)

        for record in self:
            if record.payment_state == 'paid' and record.checkout_id:

                checkout = record.checkout_id

                # Only update if still unavailable
                for line in checkout.checkout_line_ids:
                    if line.book_id and line.book_id.status != 'available':
                        line.book_id.sudo().status = 'available'

                for record in checkout:
                    if record.is_paid == False:
                        record.is_paid = True

        return res
