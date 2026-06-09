# -*- coding: utf-8 -*-
{
    'name': 'Weather Notification',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': True,

    'assets': {
        'web.assets_backend': [
            'weather_notification/static/src/js/weather_systray_icons.js',
            'weather_notification/static/src/xml/weather_systray_icons.xml',
        ],
    },
}
