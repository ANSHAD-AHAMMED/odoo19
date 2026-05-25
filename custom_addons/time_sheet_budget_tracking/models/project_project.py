# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = "project.project"
    budget = fields.Float(string="Budget")
    budget_spend = fields.Monetary(string="Budget spend", compute="_compute_budget_spend")
    send_mail = fields.Char(string="Send mail", related="user_id.email")
    reminder_sent = fields.Boolean(default=False)
    task_id = fields.Many2one('project.task',string="Task")

    @api.depends('budget_spend')
    def _compute_budget_spend(self):
        """ Compute budget spend for a project """
        total_budget = 0
        for project in self:
            tasks = self.env['project.task'].search([
                ('project_id', '=', project),
            ])

            for task in tasks:

                timesheet = self.env['account.analytic.line'].search([
                    ('task_id', '=', task.id),
                ])

                for line in timesheet:
                    line.compute_total_budget()
                    employee = self.env['hr.employee'].search([
                        ('employee_id', '=', line.employee_id)
                    ])

                    total_time = line.unit_amount

                    for cost in employee:
                        minute_cost = cost.hourly_cost / 60
                        hour_cost = minute_cost * total_time
                        total_budget = total_budget + hour_cost

            if self.budget:
                spend_budget = self.budget * 0.8

                if total_budget >= spend_budget:
                    msg = _("Budget spent is very high")
                    project.sudo().message_post(body=msg)

                    template = self.env.ref('time_sheet_budget_tracking.email_template_over_expense_reminder')
                    template.send_mail(self.id, force_send=True)
                    self.reminder_sent = True

            self.write({
                'budget_spend': total_budget if total_budget else False,
            })
