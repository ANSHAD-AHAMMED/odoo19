# -*- coding: utf-8 -*-
{
    'name': 'Sale POS Counter Payment',
    'version': '17.0.1.0.0',
    'category': 'Odoo Development',
    'summary': 'Pay Sale Orders at the POS Counter — creates a POS order from a confirmed sale order via a payment wizard.',
    'description': """
        Allows sales staff to collect payment at the POS counter directly from a
        confirmed sale order:

        * "Pay at the Counter" button on the sale order form
        * Wizard collects payment per POS payment method with live remaining balance
        * Automatically creates a validated POS order with mapped order lines & payments
        * Sale order transitions to the dedicated "Paid at Counter" state
    """,
    'author': 'Anshad ahamed',
    'depends': ['sale_management', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_pos_payment_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
