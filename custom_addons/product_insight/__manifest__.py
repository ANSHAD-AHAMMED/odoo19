# -*- coding: utf-8 -*-
{
    'name': 'Product Insight Management',
    'version': '19.0.1.0.0',
    'author': 'anshad ahammed m',
    'website': 'http://www.cybrosys.com',
    'category': 'Odoo development',
    'summary': """a module for product insight management""",
    'description': """this is description""",
    'license': 'LGPL-3',
    # 'sequence': -10,
    # 'application': True,
    'installable': True,
    'auto_install' : True,

    'depends':[
        'base',
        'product',
    ],
    #
    # # for showing datas from the views
    'data':[
        'security/ir.model.access.csv',
        'wizard/product_price_wizard_views.xml',
        'views/product_product_views.xml',
        # 'views/product_insighht_management_menu.xml',
    ]
}
