# -*- coding: utf-8 -*-
from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = "project.project"

    user_task_limit = fields.Integer(string='Task limit')
