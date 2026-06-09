# -*- coding: utf-8 -*-
from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_lan_long = fields.Boolean(string="Weather based on Lat&Lon")
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")