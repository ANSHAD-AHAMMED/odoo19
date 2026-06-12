# -*- coding: utf-8 -*-
from odoo import fields, models

class CountryPriceList(models.Model):
    _name = 'country.pricelist'
    _description = 'Country Price List'

    name = fields.Char(string='Name')
    country_id = fields.Many2one('res.country', string='Country')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
