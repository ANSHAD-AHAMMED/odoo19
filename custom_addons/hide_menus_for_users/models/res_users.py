# -*- coding: utf-8 -*-
from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    hide_menu = fields.Many2many(
        'ir.ui.menu',
        'res_users_hidden_menu_rel',
        'user_id',
        'menu_id',
        string="Hidden Menus"
    )

