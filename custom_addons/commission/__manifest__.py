# -*- coding: utf-8 -*-
{
    'name': 'Sales Commission',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Modify existing web pages through code',
    'depends': ['sale'],  # Core website and eCommerce
    'data': [
        'security/commission_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/res_user_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
