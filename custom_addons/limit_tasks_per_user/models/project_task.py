# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals_list):
        tasks = super().write(vals_list)

        assignees = self.env['project.task'].search([
            ('user_ids', 'in', self.user_ids),
            ('project_id', 'in', self.project_id),
        ])
        users = self.env['res.users'].search([])

        if assignees:
            for user in users.ids:
                tasks = 0

                for task in assignees:
                    if user in task.user_ids.ids:
                        tasks += 1

                        if tasks > self.project_id.user_task_limit:
                            raise UserError("This User reached the task limit")
        return tasks
