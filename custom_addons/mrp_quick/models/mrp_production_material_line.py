from odoo import fields, models

class MrpProductionMaterialLine(models.Model):
    _name = 'mrp.production.material.line'
    _description = 'Mrp Production Material Line'

    production_id = fields.Many2one('mrp.production.ext', string='Production')
    product_id = fields.Many2one('product.product', string="product")
    required_qty = fields.Float(string="Required Qty")
    available_qty = fields.Float(string="Available Qty")
    consumed_qty = fields.Float(string="Consumed Qty")
