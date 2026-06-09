# -*- coding: utf-8 -*-
{
    'name': 'Hide Menus for Users',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Allow configuration to hide specific menus for users, selectable from the User form.',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
