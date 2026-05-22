from odoo import fields, models, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    total_budget = fields.Float(string="Total Budget", compute='compute_total_budget')

    @api.depends('total_budget')
    def compute_total_budget(self):
        """ Compute budget spent for each employees """
        total_budget = 0.0

        for employee in self:
            total_time = employee.unit_amount
            minute_cost = employee.employee_id.hourly_cost / 60
            hour_cost = minute_cost * total_time
            total_budget = total_budget + hour_cost

            employee.write({'total_budget': total_budget})