# -*- coding: utf-8 -*-
from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_sale_id = fields.Many2one('sale.order', string='Sale Order')
    def action_sale_from_project_view(self):
        print('self.project_id:', self.project_id)
        print('self.sale_order_id', self.task_sale_id)
        consume = self.env['sale.order'].search([
            ('project_id', '=', self.sale_order_id.project_id.id),
            # ('p', '=', self.partner_id),
        ])
        # for task in consume:
        print('consume:', consume.ids)
        print('self.project_id.id:', self.project_id.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Consume',
            'res_model': 'sale.order',
            "domain": [('project_id', '=', self.project_id.id)],
            # 'res_id': consume.ids,
            # 'view_mode': 'list',' form',
            'views': [[False, 'list'], [False, 'form']],
            'target': 'current',
        }


