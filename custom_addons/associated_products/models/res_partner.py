# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    associated_product_id = fields.Many2many('product.product', string="Associated Product")