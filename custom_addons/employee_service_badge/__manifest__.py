# -*- coding: utf-8 -*-
{
    'name': 'Employee Service Badge',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Employee years-of-service badge on employee form',
    'depends': [
        'project',
        'hr_timesheet'
    ],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}