from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users' # No '_name' here

    # TO ADD A FIELD IN USERS(SETTINGS, USER,(SELECT ANY USERS)), NOT IN PROPERTY TYPE, IT'S VISIBLE IN USERS.
    # IT INHERIT properties MODEL TO USERS
    property_id = fields.One2many('properties', 'user_id', domain=[('state','=','new')])
