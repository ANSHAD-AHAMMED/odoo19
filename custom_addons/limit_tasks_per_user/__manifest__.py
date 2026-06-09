# -*- coding: utf-8 -*-
{
    'name': 'Limit number of open tasks per user',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'A user can have at most N open tasks assigned; creation/assignment blocked if exceeded.',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_project_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
