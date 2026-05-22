# -*- coding: utf-8 -*-
{
    'name': 'Restricted Product Price Changing',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Modify existing web pages through code',
    'depends': [
        'base',
        'product',
    ],  # Core website and eCommerce
    'data': [
        'security/restrict_product_price_security.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
