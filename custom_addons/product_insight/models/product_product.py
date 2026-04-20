# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    internal_remark = fields.Char(string="Internal Remark")
    discount = fields.Float(
        string="Discount",
        compute="_compute_discount"
    )
    price_category = fields.Char(
        string="Price Category",
        compute="_compute_price_category"
    )

    @api.depends('list_price')
    def _compute_discount(self):
        """ compute 10% discount """
        for product in self:
            product.discount = product.list_price*0.9

    @api.depends('list_price')
    def _compute_price_category(self):
        """ Compute price category """
        for product in self:
            if product.list_price >= 1000:
                product.price_category = "Premium"
            else:
                product.price_category = "Standard"

    def action_open_price_wizard(self):
        """ wizard open function """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'product wizard',
            'res_model': 'product.price.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'product_id': self.id
            }
        }
