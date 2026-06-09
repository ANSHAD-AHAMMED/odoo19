# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import timedelta


class ProjectProject(models.Model):
    _inherit = "project.task"

    @api.onchange("allocated_hours")
    def _compute_deadline(self):
        for task in self:
            tasks_deadline = self.allocated_hours / task.user_ids.resource_calendar_id.hours_per_day

            extra_days = 0
            for days in range(round(tasks_deadline)):
                deadline_task = self.date_assign + timedelta(days=days)
                if deadline_task.strftime("%A") == "Saturday":
                    extra_days += 2

            deadline_task = deadline_task + timedelta(days=extra_days)

            self.write({'date_deadline': deadline_task})
