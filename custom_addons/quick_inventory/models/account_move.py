# -*- coding: utf-8 -*-
from odoo import fields, models, api, Command
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    stock_picking = fields.Many2one('stock.picking', string="Stock Picking")

    @api.onchange('stock_picking')
    def onchange_stock_picking(self):
        if not self.stock_picking.move_ids:
            raise UserError('This have no lines')

        if self.stock_picking:
            print(1)
            product = []
            print(2)
            self.write({'invoice_line_ids': [Command.clear()]})
            print(5)
            for products in self.stock_picking.move_ids:
                print(6)
                product.append(Command.create({
                    'product_id': products.product_id,
                    'quantity': products.quantity
                }))
                print(7)
            print('product:',product)
            self.invoice_line_ids = product
            print(8)


