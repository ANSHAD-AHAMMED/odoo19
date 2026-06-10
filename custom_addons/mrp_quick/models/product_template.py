from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_manufacturable = fields.Boolean(string="Manufacturable")