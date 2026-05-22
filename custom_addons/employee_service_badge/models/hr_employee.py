# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    date_start = fields.Datetime(string="Start Date111", compute="_compute_date_start") #
    emp_experience = fields.Selection(
        string="Experience",
        selection=[
            ('newcomer', 'Newcomer'),
            ('rising', 'Rising'),
            ('veteran', 'Veteran'),
            ('expert', 'Expert'),
        ],
        default='newcomer', readonly=True,
    )
    anniversary = fields.Boolean(string="Anniversary", default=False)
    experience_year = fields.Integer(string="Experience Year", readonly=True)

    @api.depends('date_start')
    def _compute_date_start(self):
        if self.create_date:
            self.write({'date_start': self.create_date})

            today = fields.Datetime.today()

            expert = today - relativedelta(years=5)
            veteran = today - relativedelta(years=3)
            rising = today - relativedelta(years=1)

            year_experience = today.year - self.date_start.year
            self.write({'experience_year': year_experience})

            if self.date_start <= expert:
                self.emp_experience = 'expert'

            elif self.date_start <= veteran:
                self.emp_experience = 'veteran'

            elif self.date_start <= rising:
                self.emp_experience = 'rising'

            else:
                self.emp_experience = 'newcomer'

        if self.date_start.month == today.month:
            if self.date_start.day == today.day:
                self.write({'anniversary': True})
