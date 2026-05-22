# -*- coding: utf-8 -*-
{
    'name': 'Sales Margin',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Add Margin to Sales Order',
    'depends': [
        'sale',
        'mail',
        'sale_management',
    ],
    'data': [
        'security/sale_order_margin_security.xml',
        'views/product_category_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
