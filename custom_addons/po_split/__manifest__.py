# -*- coding: utf-8 -*-
{
    'name': 'purchase order split',
    'version': '19.0.1.0.0',
    'author': 'anshad ahammed m',
    'category': 'Odoo Development',
    'summary': """a module for split purchase orders based on lowest value""",
    'description': """this is description""",
    'license': 'LGPL-3',
    'installable': True,
    'auto_install' : True,

    'depends':[
        'base',
        'product',
        'purchase',
    ],
    'data':[
        # 'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        # 'views/res_config_settings_views.xml',
    ]
}
