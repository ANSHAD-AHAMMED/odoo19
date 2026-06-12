# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError

class HrLeave(models.Model):
    _inherit = "hr.leave"

    def action_approve(self):
        departments = self.env['hr.employee'].search([
            ('department_id', '=', self.employee_id.department_id.id)
        ])

        holidays = self.env['hr.leave'].sudo().search([
            ('department_id', 'in', self.employee_id.department_id.id),
            ('date_from', '<=', fields.Datetime.now()),
            ('date_to', '>=', fields.Datetime.now()),
            ('state', '=', 'validate'),
        ])

        half_department = len(departments) / 2
        if len(holidays) >= half_department:
            if not self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                raise UserError(f"Today many employees are leave:\n"
                                f"{holidays.employee_id.name}")

        super().action_approve()
