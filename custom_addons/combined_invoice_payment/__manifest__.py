# -*- coding: utf-8 -*-
{
    'name': 'Combained invoice payment',
    'version': '19.0.1.0.0',
    'author': 'anshad ahammed m',
    'category': 'Odoo development',
    'summary': """a module for Combained invoice payment""",
    'description': """this is description""",
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,

    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_payment_views.xml',
    ]
}