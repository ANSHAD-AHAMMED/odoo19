# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProjectProject(models.Model):
    _inherit = "project.project"

    # customer_id = fields.Many2one('res.partner', string="Customer")