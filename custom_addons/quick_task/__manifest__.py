# -*- coding: utf-8 -*-
{
    'name': "Quick task",
    'version': "19.0.1.0.0",
    'author': 'anshad ahammed m',
    'summary': """this module help to manage the library.""",
    'category': 'Odoo Development',
    'description': """this module include several models like books, authors, publishers, genrers and checkout""",
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'auto_install': True,

    'depends': [
        'base',
        'fleet',
        'hr',
        'sale',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/fleet_service_order_views.xml',
        'views/quick_task_menu.xml',
    ],

}
