# -*- coding: utf-8 -*-
from odoo import fields, models

class ComponentProducts(models.Model):
    _name = "component.products"
    _description = "Component Products"

    simple_product_id = fields.Many2one('simple.production', string="Production")
    product_id = fields.Many2one('product.product', string="Component Product")
    simple_product_bom_id = fields.Many2one('simple.product.bom', string="Bom")
    simple_product_qty = fields.Integer(string="Qty to Consume")