# -*- coding: utf-8 -*-
from odoo import fields, models

class ResUser(models.Model):
    _inherit = 'res.users'

    sale_commission_percentage = fields.Float(string='Sale Commission Percentage')