# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, Command
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _name = 'mrp.production.ext'
    _description = 'Mrp Production'

    name = fields.Char(string="Name", default=lambda self: _('New'), readonly=True, copy=False, help="Reference Number of the book")
    product_id = fields.Many2one('product.template', string='product')
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    quantity = fields.Float(string='Quantity')
    planned_date = fields.Datetime(string='Planned Date')
    material_line_ids = fields.One2many(comodel_name='mrp.production.material.line', inverse_name='production_id')
    state = fields.Selection([])
    is_available = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a new book """

        for vals in vals_list:
            # """Automatically generate a reference number for new books."""
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('mrp.production.ext')

        return super().create(vals_list)

    @api.onchange('bom_id')
    def onchange_product_id(self):
        self.write({
            'product_id': self.bom_id.product_tmpl_id,
        })

        self.write({'material_line_ids': [Command.clear()]})

        new_lines = self.env['mrp.production.material.line']

        for qty in self.bom_id.bom_line_ids:

            if qty.product_qty > qty.product_id.qty_available:
                print('productqty:', qty.product_qty)
                print('productqty_avail:', qty.product_id.qty_available)
                self.write({'is_available':False})

            else:
                self.write({'is_available': True})
            new_line = self.env['mrp.production.material.line'].new({
                'product_id': qty.product_id.id,
                'required_qty': qty.product_qty,
                'available_qty': qty.product_id.qty_available,
            })

            new_lines |= new_line

        self.material_line_ids |= new_lines

        if not self.material_line_ids:
            raise UserError('No material lines available')
