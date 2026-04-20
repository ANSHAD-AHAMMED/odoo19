# -*- coding: utf-8 -*-
{
    'name': 'Associated Products',
    'version': '19.0.1.0.0',
    'author': 'anshad ahammed m',
    'category': 'Odoo development',
    'summary': """a module for Associated Products for a partner""",
    'description': """this is description""",
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,

    'depends': [
        'base',
        'sale',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ]
}
