{
    'name': "Employee Loan Management",
    'version': "19.0.1.0",
    'author': 'anshad ahammed m',
    'summary': """this module help to manage the employee loan.""",
    'category': 'Odoo Development',
    'description': """this module include several models like employee loan, employee loan line""",
    'license': "LGPL-3",
    'application': True,
    'installable': True,

    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'data/employee_loan_sequence_data.xml',
        'views/employee_loan_views.xml',
        'views/employee_loan_management_menu.xml',
    ]

}
