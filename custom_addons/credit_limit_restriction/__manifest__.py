# -*- coding: utf-8 -*-
{
    'name': 'Creadit Limit Restriction',
    'version': '19.0.1.0.0',
    'author': 'anshad ahammed m',
    'category': 'Odoo development',
    'summary': """a module for Dynamic credit limit restriction""",
    'description': """this is description""",
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,

    'depends': [
        'base',
        'sale',
        'sale_management',
    ],
    'data': [
        'views/res_config_settings_views.xml'
    ]
}
