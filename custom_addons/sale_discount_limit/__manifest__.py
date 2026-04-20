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

# 1. Set maximum discount limit for a month in the Settings -> Sales -> Pricing.
# 2. Check the total discount of the month is exceed the limit. If it exceed show the warning message.
# i have done the first task, now we need to do second task, in sales_order_line.py there is a function for discount, its available in "https://github.com/odoo/odoo", the function name is "_compute_discount", field name is "discount"