from odoo import api, fields, models, tools

class ProjectTask(models.Model):
    _inherit = "project.task"

    allowed_hours = fields.Float(string="Allowed Hours")
    total_logged_hours = fields.Float(string="Total Logged Hours")
    over_budget = fields.Boolean(string="Over Budget", default=False)
