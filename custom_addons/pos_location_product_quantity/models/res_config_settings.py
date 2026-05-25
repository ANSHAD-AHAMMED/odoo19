# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_in_location = fields.Many2one(
        'stock.location',
        String='Product In Location',
        config_parameter='pos_location_product_quantity.product_in_location',
    )
