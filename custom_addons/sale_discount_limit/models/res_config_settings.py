# -*- coding: utf-8 -*-
from odoo import fields, models

class ResSettings(models.TransientModel):
    _inherit = "res.config.settings"

    discount_limit = fields.Float(
        string="Discount Limit",
        config_parameter='sale_discount_limit.discount_limit',
        default=2,
        help="The discount limit for sale in a month"
    )
