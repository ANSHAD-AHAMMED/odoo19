# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'

    name = fields.Char(
        string="Name",
        default=lambda self: _('New'),
        copy=False)
    # name = fields.Char(string='Name')
    employee_id = fields.Many2one('hr.employee')
    loan_amount = fields.Float(string='Loan Amount')
    installment_count = fields.Integer(string='Installment Count')
    start_date = fields.Date(string='Start Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('ongoing', 'Ongoing'),
        ('paid', 'Paid'),
    ])

    loan_line_ids = fields.One2many('employee.loan.line','loan_id')


    @api.model_create_multi
    def create(self, vals_list):
        """ Create reference number for the Employee Loan """
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.loan')
        return super().create(vals_list)




