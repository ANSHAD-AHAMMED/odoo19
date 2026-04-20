from odoo import fields,models
import random

class property_tags(models.Model):
    _name = 'property_tags'
    _description = 'property tags for filtering'
    _order = "name"

    name = fields.Char(string='Property Tag')
    color = fields.Integer('Color Index', default=lambda self: random.randint(1,11)) #TO ADD RANDOM COLORS FOR THE TAGS
    # color = fields.Integer(string='Color', random=True)

    _check_property_tags = models.Constraint(
        'unique(name)',
        'The tag must be unique.',
    )