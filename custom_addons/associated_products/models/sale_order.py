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
            print('associated_products=', associated_products)
            associated_product_ids = associated_products.ids
            print('associated_product_ids=', associated_product_ids)

            if order.associated_product:
                existing_product_ids = order.order_line.mapped('product_id.name')
                print('existing_product_ids=', existing_product_ids)
                new_lines = self.env['sale.order.line']
                print('new_lines=', new_lines)
                for product in associated_products:
                    if product.id not in existing_product_ids:
                        new_line = self.env['sale.order.line'].new({
                            'order_id': order.id,
                            'product_id': product.id,
                            'product_uom_qty': 1,
                            'is_associate': True,
                        })
                        new_lines |= new_line
                        print('new_line=', new_line)
                        print('new_lines=', new_lines)
                order.order_line |= new_lines
                print('order.order_line=', order.order_line)

            # else:
            #     order.order_line = order.order_line.filtered(
            #         lambda l: l.product_id.id not in associated_product_ids
            #     )
            #     print('else:')
            #     print('order.order_line=', order.order_line)
