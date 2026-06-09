# -*- coding: utf-8 -*-
{
    'name': 'QR Code Generator',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'depends': [
        'base',
    ],

    'installable': True,
    'auto_install': True,

    'assets': {
        'web.assets_backend': [
            'qr_code_generator/static/src/js/qr_code_generator.js',
            'qr_code_generator/static/src/xml/qr_code_generator.xml',
            'qr_code_generator/static/lib/qrcode.js',
        ],
    },

}
