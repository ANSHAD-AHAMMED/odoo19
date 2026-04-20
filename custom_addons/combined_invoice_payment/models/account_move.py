# -*- coding: utf-8 -*-
from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_payment_amount = fields.Float(string="Payment Amount")
