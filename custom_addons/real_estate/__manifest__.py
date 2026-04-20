{
    'name': 'real_estate',
    'version': '19.0.1.0',
    'author': 'anshad ahammed m',
    'website': 'http://www.cybrosys.com',
    'category': 'Economics',
    'summary': """hi hello world""",
    'description': """this is description""",
    'license': 'LGPL-3',
    # 'sequence': -10,
    'application': True,
    'installable': True,
    # 'auto_install' : True,

    'depends': ['sale_management','purchase'],

    # for showing datas from the views
    'data': [
        'security/ir.model.access.csv',
        'views/property_offers_views.xml',
        'views/property_views.xml',
        'views/property_tags_views.xml',
        'views/property_types_views.xml',
        'views/user_model_inheritance.xml',
        'views/abin_task.xml',
        'views/real_estate_menu.xml',
    ]
}
