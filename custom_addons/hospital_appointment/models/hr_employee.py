# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    appointment_id = fields.Many2one('hospital.appointment',string="Appointment")
    is_doctor = fields.Boolean(string="Doctor")
    specialization = fields.Char(string="Specialization")
    is_available = fields.Boolean(string="Available")
    treatment_progress = fields.Float(string="Treatment Progress", compute="_compute_treatment_progress")

    @api.depends('appointment_id.state')
    def _compute_treatment_progress(self):
        """ Compute treatment progress """
        appointments = self.env['hospital.appointment'].search([
            ('doctor_id', 'in', self.id),
        ])
        completed_appointments = appointments.filtered(lambda completed: completed.state == 'completed')
        if appointments:
            progress = len(completed_appointments) / len(appointments) * 100
            self.write({'treatment_progress': progress})
        else:
            self.write({'treatment_progress': 0})
