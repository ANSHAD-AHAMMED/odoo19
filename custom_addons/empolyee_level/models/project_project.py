# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    task_id = fields.Many2one('project.task.type',string="Task")
    project_id = fields.Many2one('project.task',string="Project")
    project_task_ids = fields.Many2many('project.task.type', string="Tasks")


    def generate_timesheet(self):
        tasks = self.env['project.task'].search([
            ('project_id', '=', self.id),
            ('active', '=', True),
        ])

        for task in tasks:
            allowed_hours = task.allowed_hours
            total_logged_hours = task.effective_hours
            over = total_logged_hours - allowed_hours
            over_budget = over / 100
            if over_budget >= 2:
                task.write({
                    'over_budget': True,
                    'total_logged_hours':total_logged_hours
                })
            else:
                if not over_budget:
                    for user in task.user_ids:
                        if user.employee_id.add_timesheet_automatically:
                            new_line = self.env['account.analytic.line'].new({
                                'date': fields.Date.today(),
                                'employee_id': user.employee_id.id,
                                'unit_amount': 10.00,
                                'name':"automatic generation",
                            })
                            task.write({
                                'total_logged_hours': total_logged_hours
                            })
                            task.timesheet_ids |= new_line
