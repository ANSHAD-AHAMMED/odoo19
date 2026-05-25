# -*- coding: utf-8 -*-
{
    'name': 'POS Location Product Quantity',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'display available product quantity in the location specified in POS settings.',
    'depends': [
        'point_of_sale',
        'stock'
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': True,

    'assets': {

        'point_of_sale._assets_pos': [
            'pos_location_product_quantity/static/src/**/*',
        ],
    },
}

