# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_rating = fields.Selection(
        string="Product Rating",
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        default='1'
    )

    @api.model
    def _load_pos_data_fields(self, config):
        """ Adds the 'product_rating' field to the list of fields loaded into the POS. """
        data = super()._load_pos_data_fields(config)
        data += ['product_rating']
        return data