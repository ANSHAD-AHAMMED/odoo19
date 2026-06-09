# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class FleetServiceOrderPart(models.Model):
    _name = 'fleet.service.order.part'
    _description = 'Fleet Service Order Part'

    order_id = fields.Many2one('fleet.service.order', string='Order')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    unit_price = fields.Float(string='Unit Price', compute='_compute_unit_price')

    @api.depends('product_id')
    def _compute_unit_price(self):
        """ Compute unit price """
        for order in self.order_id:
            for line in order.part_ids:
                line.unit_price = line.product_id.lst_price
