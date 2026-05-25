# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosSession(models.Model):
    _inherit = "pos.session"

    def clear_line(self):
        print('kokokokokokok')
