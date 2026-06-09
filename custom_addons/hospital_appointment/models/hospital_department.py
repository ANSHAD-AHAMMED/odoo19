from odoo import fields, models, api

class HospitalDepartment(models.Model):
    _name = "hospital.department"
    _description = "Hospital Department"

    name = fields.Char(string="Name")
    doctor_ids= fields.Many2many('hr.employee',string="Doctors")