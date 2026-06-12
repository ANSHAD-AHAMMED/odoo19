# -*- coding: utf-8 -*-
{
    'name': 'Empolyee Level',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Employee years-of-service badge on employee form',
    'depends': [
        'project',
        'hr_timesheet'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_level_views.xml',
        'views/hr_employee_views.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/employee_level_menu.xml',
    ],
    'installable': True,
    'auto_install': True,
}