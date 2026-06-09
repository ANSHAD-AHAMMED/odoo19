# -*- coding: utf-8 -*-
{
    'name': 'Quiz - Idle timer',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',

    'depends': [
        'base',
        'web',
        'survey',
    ],

    'data': [
        'views/survey_survey_views.xml',
        'views/survey_templates.xml',
    ],
    'installable': True,
    'auto_install': True,

    'assets': {
        'survey.survey_assets': [
            'quiz_idle_timer/static/src/js/idle_timer.js',
        ]
    },
}
