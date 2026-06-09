# -*- coding: utf-8 -*-
from odoo import models, api, fields

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    user_id = fields.Many2one('res.users', string='User')

    @api.depends('user_id.hide_menu')
    def _filter_visible_menus(self):
        """ Hide menus From the users. """
        visible = super()._filter_visible_menus()
        hidden = self.env.user.hide_menu

        if hidden:
            visible = visible - hidden

        return visible
