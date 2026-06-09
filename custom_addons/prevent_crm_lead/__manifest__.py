# -*- coding: utf-8 -*-
{
    'name': 'Prevent CRM Lead',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Prevent a CRM lead from reaching "Won" without a meeting',
    'depends': [
        'crm',
    ],
    'data': [
        'security/prevent_crm_lead_security.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
