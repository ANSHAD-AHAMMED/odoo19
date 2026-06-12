# -*- coding: utf-8 -*-
{
    'name': 'Vendor Price Variance Control',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Project budget tracking with timesheet cost alerts',
    'depends': [
        'purchase',
        # 'hr_timesheet'
    ],
    'data': [
        # 'data/over_expense_reminder.xml',
        'views/purchase_order_views.xml',
        # 'views/project_project_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
