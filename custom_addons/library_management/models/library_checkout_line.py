# -*- coding: utf-8 -*-
from odoo import fields, models

class libraryCheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _description = 'Library Checkout Line'

    checkout_id = fields.Many2one('library.checkout', string="Book")
    partner_id = fields.Many2one('res.partner', string="Customer")
    book_id = fields.Many2one(
        'library.book',
        string="Book",
        domain="[('status', '!=', 'unavailable')]")

    price = fields.Float(related="book_id.price",string="Price")
    penalty = fields.Float(string="Penalty", related="checkout_id.penalty", store=True)

    checkout_date = fields.Datetime(string="Checkout Date", related="checkout_id.checkout_date", store=True)
    due_date = fields.Datetime(string="Due Date", related="checkout_id.due_date", store=True)
    return_date = fields.Datetime(string="Return Date", related="checkout_id.return_date", store=True)

    is_late = fields.Boolean(string="Late", related="checkout_id.is_late", store=True)
