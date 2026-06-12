# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_level_id = fields.Many2one('employee.level', string='Employee Level')
    flag = fields.Boolean(string='Flag', default=False)
    salary = fields.Float(string='Salary', default=0, related='employee_level_id.salary')
    add_timesheet_automatically = fields.Boolean(string='Automatically Add Timesheet', default=False)


    @api.onchange('employee_level_id')
    def onchange_employee_level_id(self):
        employee = self.env['employee.level'].search([]).mapped('level')
        if self.employee_level_id.level != max(employee):
            self.flag = False
        if self.employee_level_id.level == max(employee):
            self.flag = True

    def action_employee_level_increment(self):
        now = self.employee_level_id.level+1
        emp = self.env['employee.level'].search([]).mapped('level')

        employee = self.env['employee.level'].search([
            ('level', '=', now),
        ])
        if employee:
            self.write({
                'employee_level_id': employee.id,
            })

        if self.employee_level_id.level == max(emp):
            self.flag = True

