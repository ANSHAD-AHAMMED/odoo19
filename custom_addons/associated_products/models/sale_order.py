# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    associated_product = fields.Boolean(string="Associated Product")

    @api.onchange('associated_product')
    def associate_product(self):
        """ add or remove associated product from sale order """
        for order in self:
            associated_products = order.partner_id.associated_product_id
            # associated_product_ids = associated_products.ids

            if order.associated_product:
                existing_product_ids = order.order_line.mapped('product_id.name')
                new_lines = self.env['sale.order.line']
                for product in associated_products:
                    if product.id not in existing_product_ids:
                        new_line = self.env['sale.order.line'].new({
                            'order_id': order.id,
                            'product_id': product.id,
                            'product_uom_qty': 1,
                            'is_associate': True,
                        })
                        new_lines |= new_line
                order.order_line |= new_lines
