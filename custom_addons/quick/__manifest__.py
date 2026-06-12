# -*- coding: utf-8 -*-
{
    'name': 'Sale Quick',
    'version': '19.0.1.0.0',
    'category': 'Odoo Development',
    # 'summary': 'Create a simple tool for producing some products by consuming some other products(like BoM/Components) without using manufacturing',
    'depends': [
        'base',
        'sale',
        'project',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_project_views.xml',
        'views/sale_order_views.xml',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
