# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    add_product_ids = fields.Many2many('product.product', string="Associated Product")