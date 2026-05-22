# -*- coding: utf-8 -*-
{
    'name': 'POS Rating',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Project budget tracking with timesheet cost alerts',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'auto_install': True,

    'assets': {

        'point_of_sale._assets_pos': [
            'pos_rating/static/src/**/*',
        ],
    },
}
