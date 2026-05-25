# -*- coding: utf-8 -*-
{
    'name': 'Time Sheet Budget Tracking',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Project budget tracking with timesheet cost alerts',
    'depends': [
        'project',
        'hr_timesheet'
    ],
    'data': [
        'data/over_expense_reminder.xml',
        'views/account_analytic_line_views.xml',
        'views/project_project_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
