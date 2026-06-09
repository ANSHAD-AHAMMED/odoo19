# -*- coding: utf-8 -*-
from odoo import fields, models

class BomComponentProducts(models.Model):
    _name = "bom.component.products"
    _description = "Bom Component Products"

    simple_product_id = fields.Many2one('simple.production', string="Production")
    product_id = fields.Many2one('product.product', string="Component Product")
    simple_product_bom_id = fields.Many2one('simple.product.bom', string="Bom")
    simple_product_bom_qty = fields.Integer(string="Qty to Consume")