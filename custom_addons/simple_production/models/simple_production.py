# -*- coding: utf-8 -*-
from odoo import fields, models, _, api, Command
from odoo.exceptions import ValidationError


class SimpleProduction(models.Model):
    _name = 'simple.production'
    _description = 'Simple Production'

    name = fields.Char(string='Production Name')
    product_id = fields.Many2one('product.product', string="Finished Product")
    product_qty = fields.Integer(string="Qty to Produce", default=1)
    component_ids = fields.One2many('component.products', inverse_name='simple_product_id')
    simple_product_bom_ids = fields.One2many('simple.product.bom', inverse_name='simple_product_id', string="Bom")


    @api.onchange('product_qty')
    def onchange_product_qty(self):
        """ Change Components quantity based on product qty """
        for qty in self.component_ids:
            bom_product = self.env['simple.product.bom'].search([
                ('product_id', '=', self.product_id.id),
            ], limit=1)

            for q in bom_product.bom_component_ids:
                if qty.product_id.id == q.product_id.id:
                    quantity = self.product_qty * q.simple_product_bom_qty
                    qty.write({'simple_product_qty': quantity})

    @api.onchange('product_id')
    def product_bom(self):
        """ create component line """
        self.write({'component_ids': [Command.clear()]})
        bom_product = self.env['simple.product.bom'].search([
            ('product_id', '=', self.product_id.id),
        ],limit=1)

        new_lines = self.env['component.products']

        for qty in bom_product.bom_component_ids:
            new_line = self.env['component.products'].new({
                'product_id': qty.product_id.id,
                'simple_product_qty': qty.simple_product_bom_qty,
            })
            new_lines |= new_line

        self.component_ids |= new_lines

    def update_stock(self):
        """ Update stock quantities """
        location = self.env.ref('stock.stock_location_stock')
        if self.product_id and self.product_qty:
            self.env['stock.quant']._update_available_quantity(
                self.product_id,
                location,
                self.product_qty,
            )

        for comp in self.component_ids:
            if not comp.product_id or not comp.simple_product_qty:
                continue

            quant = self.env['stock.quant'].search([
                ('product_id', '=', comp.product_id.id),
                ('location_id', '=', location.id),
            ], limit=1)

            available = quant.quantity if quant else 0

            if available < comp.simple_product_qty:
                raise ValidationError("not enough stock for component")

            self.env['stock.quant']._update_available_quantity(
                comp.product_id,
                location,
                -comp.simple_product_qty,
            )

    @api.model_create_multi
    def create(self, vals):
        """ Create a new record """
        records = super().create(vals)
        return records
