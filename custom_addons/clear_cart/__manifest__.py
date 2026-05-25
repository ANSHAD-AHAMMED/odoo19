# -*- coding: utf-8 -*-
{
    'name': 'Clear Cart',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Modify existing web pages through code',
    'depends': ['website', 'website_sale'],  # Core website and eCommerce
    'data': [
        'views/clear_cart_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
