# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'
    _description = 'Employee Loan Line'

    loan_id = fields.Many2one(comodel_name='employee.loan')
    date = fields.Datetime(string='Date of Loan')
    amount = fields.Float(string='Amount')
    paid = fields.Boolean(string='Paid')