# -*- coding: utf-8 -*-
{
    'name': 'POS Quick',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'depends': [
        'point_of_sale',
        'stock',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/button_pay_wizard.xml',
    ],
    'installable': True,
    'auto_install': True,
}
