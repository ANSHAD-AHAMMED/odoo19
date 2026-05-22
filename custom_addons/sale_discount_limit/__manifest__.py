# -*- coding: utf-8 -*-
{
    'name': 'Discount Limit',
    'version': '19.0.1.0.0',
    'author': 'anshad ahammed m',
    'category': 'Sales',
    'summary': """a module for sales discount limit""",
    'description': """this is description""",
    'license': 'LGPL-3',
    'installable': True,
    'auto_install' : True,

    'depends':[
        'base',
        'product',
        'sale',
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ]
}
