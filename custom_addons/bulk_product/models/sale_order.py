# -*- coding: utf-8 -*-
from odoo import api, fields, models,Command
from odoo.cli import command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bulk_product_ids = fields.Many2many('bulk.product', string="Products")
    # product_ids = fields.Many2many('product.product', string="Products")
    # order_line_ids = fields.Many2many('sale.order.line', string="Order Lines")

    # product = fields.Char(string="Products")
    # product_uom_qty = fields.Float(string="Quantity")

    def add_to_order_line(self):
        for record in self:
            products = record.bulk_product_ids
            print('products=',products)

            if products:
                existing_product_ids = record.bulk_product_ids.mapped('product_id.id')
                print('existing_product_ids=',existing_product_ids)
                new_lines = self.env['sale.order.line'].mapped('product_id')

                for product in products:
                    if product.id not in existing_product_ids:
                        new_line = self.env['sale.order.line'].new({
                            # 'order_id': order.id,
                            'product_id': product.product_id.id,
                            'product_uom_qty': product.product_uom_qty,
                            # 'is_associate': True,
                        })

                        new_lines |= new_line
                    record.order_line |= new_lines
                    self.write({'bulk_product_ids': [Command.clear()]})

            # else:
            #     record.order_line = record.order_line.filtered(
            #         lambda l: l.product_id.id not in associated_product_ids
            #     )