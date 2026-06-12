# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import timedelta, date


class ProjectTask(models.Model):
    _inherit = 'project.project'

    task_id = fields.Many2one('project.task.type',string="Task")
    project_id = fields.Many2one('project.task',string="Project")
    project_task_ids = fields.Many2many('project.task.type', string="Tasks", compute='compute_task_ids')

    @api.depends('project_id')
    def compute_task_ids(self):
        person = self.task_ids.stage_id.ids
        self.write({
            'project_task_ids': person
        })

    def archive_project(self):
        """ To Archive task based on it's the timesheet """
        is_archive = self.env['ir.config_parameter'].sudo().get_param(
            'auto_archive_stale_project.archive_project'
        )
        today = date.today()
        archive_date = timedelta(days=30)
        archive_task = today - archive_date
        projects = self.env['project.project'].search([])

        if is_archive:
            for project in projects:
                tasks = self.env['project.task'].search([
                    ('project_id', '=', project),
                    ('stage_id', '=', project.task_id.id),
                ])

                for task in tasks:
                    task_active = False
                    timesheet = self.env['account.analytic.line'].search([
                        ('task_id', '=', task.id),
                    ]).mapped('date')

                    for line in timesheet:
                        if line <= archive_task:
                            task_active = True
                        else:
                            task_active = False
                            break

                    if task_active:
                        task.active = 0
                        msg = _("The task is archived due to not have a timesheet in 30days:%s", task.name)
                        project.sudo().message_post(body=msg)
