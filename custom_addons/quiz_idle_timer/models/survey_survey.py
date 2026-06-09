from odoo import fields, models, _


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    timer = fields.Float(string="Timer")
