# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_ids = fields.One2many('project.project', 'sale_order_id', string="Projects")
    project_id = fields.Many2one('project.project', string="Project")

    @api.onchange("partner_id")
    def create_project_for_partner(self):
        project = self.env["project.project"].search([("partner_id", "=", self.partner_id)])
        self.write({
            'project_ids': project
        })

    def generate_tasks_sale(self):
        if not self.project_id.task_ids:
            print(111)
            print(self.project_id)
            task1 = self.env['project.task'].create({
                'name': self.id,
                'project_id': self.project_id.id,
            })
            print(222)

            for task in self.order_line:
                self.env['project.task'].create({
                    'name': task.name,
                    'project_id': self.project_id.id,
                    'allocated_hours': 500.0,
                    'parent_id': task1.id,
                })

    def action_project_task_view(self):
        # self.ensure_one()
        consume = self.env['project.task'].search([
            ('project_id', '=', self.project_id.id),
            # ('p', '=', self.partner_id),
        ])
        # for task in consume:
        print('consume:', consume.ids)
        print('self.project_id.id:', self.project_id.id)
        print('sale:', self.id)
        # print('consume111:', consume.ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Consume',
            'res_model': 'project.task',
            "domain": [('project_id', 'in', consume)],
            # 'res_id': consume.ids,
            # 'view_mode': 'list',' form',
            'views': [[False, 'list'], [False, 'form']],
            'target': 'current',
        }

