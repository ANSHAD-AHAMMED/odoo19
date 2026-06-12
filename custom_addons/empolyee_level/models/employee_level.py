# -*- coding: utf-8 -*-
from odoo import fields, models

class EmployeeLevel(models.Model):
    _name = 'employee.level'
    _description = 'Employee Level'
    _rec_name = 'level'

    level = fields.Integer(string='Employee Level', default=1)
    salary = fields.Float(string='Salary')
