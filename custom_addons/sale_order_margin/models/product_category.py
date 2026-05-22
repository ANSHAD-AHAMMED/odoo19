# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = "product.category"

    minimum_margin_percent = fields.Float(string="Minimum Margin Percentage", default=15.0)