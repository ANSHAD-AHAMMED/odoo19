# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_rating = fields.Selection(related="product_tmpl_id.product_rating", string="Rating")
