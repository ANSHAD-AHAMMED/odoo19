# -*- coding: utf-8 -*-
from odoo import api, fields, models, Command

class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.onchange('partner_id')
    def associate_product(self):
        if self.partner_id:
            self.write({'order_line': [Command.clear()]})
            for order in self:
                add_product = order.partner_id.add_product_ids.filtered(lambda p: p.is_available == True)
                existing_product_ids = order.order_line.mapped('product_id')
                # existing_product_ids = order.order_line.filtered(lambda p: p.is_available 1000)
                new_lines = self.env['sale.order.line']
                for product in add_product:
                    if product not in existing_product_ids:
                        # if product.is_available:
                        new_line = self.env['sale.order.line'].new({
                            'order_id': order.id,
                            'product_id': product.id,
                            'product_uom_qty': 1,
                            # 'is_associate': True,
                        })
                        new_lines |= new_line
                order.order_line |= new_lines

        else:
            self.write({'order_line': [Command.clear()]})
