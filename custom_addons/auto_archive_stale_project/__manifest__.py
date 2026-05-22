# -*- coding: utf-8 -*-
{
    'name': 'Auto-archive Stale Project',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'uto-archive stale Project tasks via scheduled actionr',
    'depends': [
        'sale',
        'mail',
        'project',
        'hr_timesheet'
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/project_task_views.xml',
        'data/task_archive_action.xml',
    ],
    'installable': True,
    'auto_install': True,
}
