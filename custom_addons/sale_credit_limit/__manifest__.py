# -*- coding: utf-8 -*-
{
    'name': 'Sales Credit Limit',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Add Sales Credit Limit to Sales Order',
    'depends': [
        'sale',
        'mail',
        'sale_management',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}