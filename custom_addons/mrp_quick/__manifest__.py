# -*- coding: utf-8 -*-
{
    'name': "MRP Quick",
    'version': "19.0.1.0.0",
    'author': 'anshad ahammed m',
    'summary': """this module help to manage the library.""",
    'category': 'Odoo Development',
    'description': """this module include several models like books, authors, publishers, genrers and checkout""",
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'auto_install': True,

    'depends': [
        'base',
        'mrp',
        'stock',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/mrp_production_ext_views.xml',
        'views/product_template_views.xml',
        # 'views/mrp_production_material_line_views.xml',
        'views/mrp_production_menu.xml',
    ],

}
