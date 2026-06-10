from odoo import fields, models

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    production_id = fields.Many2one('mrp.production.ext', string='Production')
