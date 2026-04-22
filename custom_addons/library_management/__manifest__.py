# -*- coding: utf-8 -*-
{
    'name': "Library Management",
    'version': "19.0.1.0.0",
    'author': 'anshad ahammed m',
    'summary': """this module help to manage the library.""",
    'category': 'Odoo Development',
    'description': """this module include several models like books, authors, publishers, genrers and checkout""",
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'sequence': -10,

    'depends': [
        'base',
        'mail',
        'product',
        'account',
    ],

    'data': [
        'security/library_management_security.xml',
        'security/ir.model.access.csv',
        'wizard/library_report__wizard_views.xml',
        'wizard/suggestion_wizard_views.xml',
        'data/library_genre_data.xml',
        'data/due_date_reminder_template_data.xml',
        'data/over_due_reminder_template_data.xml',
        'data/ir_cron_data.xml',
        'views/library_books_views.xml',
        'views/library_author_views.xml',
        'views/library_publisher_views.xml',
        'views/library_genre_views.xml',
        'views/library_checkout_views.xml',
        'views/library_tag_views.xml',
        'views/library_settings_views.xml',
        'views/res_partner_views.xml',
        'report/library_management_report_template.xml',
        'views/library_management_menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'library_management/static/src/js/action_manager.js',
        ],
    },
}
