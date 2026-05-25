# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_location = fields.Char(string='Location')
    product_location_qty = fields.Float(string='Quantity')

    def _compute_product_in_location(self):
        product_in_location = self.env['ir.config_parameter'].sudo().get_param(
            'pos_location_product_quantity.product_in_location'
        )

        products = self.env['stock.quant'].search([
            ('location_id','=',int(product_in_location)),
        ])
        for product in products:
            product.product_id.write({
                'product_location': product.location_id.name,
                'product_location_qty':product.inventory_quantity_auto_apply
            })

    @api.model
    def _load_pos_data_fields(self, config):
        """ Adds the 'product_rating' field to the list of fields loaded into the POS. """
        self._compute_product_in_location()
        data = super()._load_pos_data_fields(config)
        data += ['product_location','product_location_qty']
        return data
