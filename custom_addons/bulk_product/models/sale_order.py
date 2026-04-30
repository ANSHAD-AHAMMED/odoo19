# -*- coding: utf-8 -*-
from odoo import fields, models,Command
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bulk_product_ids = fields.One2many('bulk.product','sale_order_id', string="Products")

    def add_to_order_line(self):
        """ Add product to order line """
        for record in self:
            for bulk in record.bulk_product_ids:
                if bulk.product_uom_qty <= 0:
                    raise UserError("All products must have at least one quantity")

                product = bulk.product_id
                print('product=',product)
                existing_line = record.order_line.filtered(lambda l: l.product_id.id == product.id)

                if existing_line:
                    existing_line.product_uom_qty += bulk.product_uom_qty

                else:
                    self.env['sale.order.line'].create({
                        'order_id': record.id,
                        'product_id': product.id,
                        'product_uom_qty': bulk.product_uom_qty,
                    })
                record.write({'bulk_product_ids': [Command.clear()]})
