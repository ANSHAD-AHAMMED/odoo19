# -*- coding: utf-8 -*-
{
    'name': "Hospital Appointment",
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
        'hr',
        'sale',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hospital_appointment_views.xml',
        'views/hospital_department_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_appointment_menu.xml',
    ],

}
