# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SimpleProductBom(models.Model):
    _name = 'simple.product.bom'
    _description = 'Simple Product Bom'

    product_id = fields.Many2one('product.product', string='Product')
    bom_component_ids = fields.One2many('bom.component.products', inverse_name='simple_product_bom_id')
    simple_product_id = fields.Many2one('simple.production', string="Production")




