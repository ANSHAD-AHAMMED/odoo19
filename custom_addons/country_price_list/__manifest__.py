# -*- coding: utf-8 -*-
{
    'name': 'Country Based Price List',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Add Country Based Price List for Customers',
    'depends': [
        'sale',
        'mail',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/country_pricelist_views.xml',
        'views/coutry_pricelist_menu.xml',
    ],
    'installable': True,
    'auto_install': True,
}
