from odoo import fields, models, api

class MrpProductionMaterialLine(models.Model):
    _name = 'mrp.production.material.line'
    _description = 'Mrp Production Material Line'
    # _rec_name = 'product_id.name'

    production_id = fields.Many2one('mrp.production.ext', string='Production')
    product_id = fields.Many2one('product.product', string="product")
    name = fields.Char(string="Name", related="product_id.name")
    bom_id = fields.Many2one('mrp.bom', string="BOM")
    required_qty = fields.Float(string="Required Qty")
    available_qty = fields.Float(string="Available Qty")
    consumed_qty = fields.Float(string="Consumed Qty")
    remaining_qty = fields.Float(string="Remaining Qty")

    # @api.onchange('consumed_qty')
    # def onchange_production_id(self):
    #     for line in self:
    #         remainig =  line.available_qty = line.consumed_qty
    #         print('remainig: ', remainig)
    #         line.write({'remaining_qty': remainig})

