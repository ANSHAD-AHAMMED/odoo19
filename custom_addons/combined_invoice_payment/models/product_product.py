from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    is_available = fields.Boolean(string="Is Available")