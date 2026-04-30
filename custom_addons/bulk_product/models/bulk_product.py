# -*- coding: utf-8 -*-
from odoo import fields, models, api

class BulkProduct(models.Model):
    _name = 'bulk.product'
    _description = 'Bulk Product'

    product_id = fields.Many2one('product.product', string="Products")
    product_uom_qty = fields.Float(string="Quantity")
    sale_order_id = fields.Many2one('sale.order', string="Sales Order")

