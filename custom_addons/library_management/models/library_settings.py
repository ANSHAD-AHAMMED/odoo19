# -*- coding: utf-8 -*-
from odoo import fields,models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reminder_days = fields.Integer(
        string="Reminder Days Before Due",
        config_parameter='library_management.reminder_days',
        default=2
    )

    penalty_per_hour = fields.Integer(
        string="Penalty per Hour",
        default=1.0,
        config_parameter='library_management.penalty_per_hour',
        help="Penalty per Hour"
    )

    max_borrow_days = fields.Integer(
        string="Default Checkout Validity",
        default=30,
        config_parameter = 'library_management.max_borrow_days',
        help="Days between checkout and expiration."
             " 0 days means automatic expiration is disabled",
    )

    maximum_borrow_books = fields.Integer(
        string="maximum borrow books for a person",
        config_parameter='library_management.maximum_borrow_books',
        default=1
    )

    max_late_returns = fields.Integer(
        string="Maximum Late Returns",
        config_parameter='library_management.max_late_returns',
        default=1
    )