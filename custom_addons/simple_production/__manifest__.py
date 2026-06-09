# -*- coding: utf-8 -*-
{
    'name': 'Simple Production',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Create a simple tool for producing some products by consuming some other products(like BoM/Components) without using manufacturing',
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/simple_production_views.xml',
        'views/simple_product_bom_views.xml',
        'views/simple_production_menu_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
