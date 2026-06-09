# -*- coding: utf-8 -*-
{
    'name': 'POS Remove order lines',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Remove each lines from selected order by simply clicking X button or clear all order with a single click.',
    'depends': [
        'point_of_sale',
    ],
    'data': [
    ],
    'installable': True,
    'auto_install': True,

    'assets': {

        'point_of_sale._assets_pos': [
            'pos_remove_order_lines/static/src/xml/order_line_delete_icon.xml',
            'pos_remove_order_lines/static/src/xml/order_line_clear_all.xml',
            'pos_remove_order_lines/static/src/js/order_line_delete_icon.js',
            'pos_remove_order_lines/static/src/js/order_line_clear_all.js',
        ],
    },
}
