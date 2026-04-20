from odoo import api, fields, models, tools

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_associate = fields.Boolean(string="Associated Product")