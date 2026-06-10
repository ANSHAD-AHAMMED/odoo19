# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, Command
from odoo.exceptions import UserError
import math


class MrpProduction(models.Model):
    _name = 'mrp.production.ext'
    _description = 'Mrp Production'

    name = fields.Char(string="Name", default=lambda self: _('New'), readonly=True, copy=False, help="Reference Number of the book")
    product_id = fields.Many2one('product.template', string='product')
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    quantity = fields.Float(string='Quantity', default=1)
    planned_date = fields.Datetime(string='Planned Date')
    material_line_ids = fields.One2many(comodel_name='mrp.production.material.line', inverse_name='production_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ],default='draft',string='Status')
    is_available = fields.Boolean(default=True)
    consumed_products = fields.Integer(string='Consumed Products')
    produced_qty = fields.Float(string='Produced Qty')

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a new book """

        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('mrp.production.ext')

        return super().create(vals_list)

    @api.onchange('product_id')
    def _compute_bom_ids(self):
        if self.product_id:
            bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_id.id)])

            if not bom:
                raise UserError('The BOM does not exist')

            # self.write({'bom_id': [Command.clear()]})
            self.write({
                'bom_id': bom,
            })

    @api.onchange('bom_id')
    def onchange_bom_id(self):
        self.write({
            'product_id': self.bom_id.product_tmpl_id,
        })

        self.write({'material_line_ids': [Command.clear()]})

        # new_lines = self.env['mrp.production.material.line']

        for qty in self.bom_id.bom_line_ids:

            if qty.product_qty > qty.product_id.qty_available:
                self.write({'is_available':False})

            else:
                self.write({'is_available': True})
            # new_line = self.env['mrp.production.material.line'].new({
            #     'product_id': qty.product_id.id,
            #     'required_qty': qty.product_qty,
            #     'available_qty': qty.product_id.qty_available,
            # })
            self.update({
                'material_line_ids':[(fields.Command.create({
                    'product_id':qty.product_id.id,
                    'required_qty': qty.product_qty,
                    'available_qty': qty.product_id.qty_available,
                }))]
            })

    @api.onchange('quantity')
    def onchange_quantity(self):
        for qty in self.material_line_ids:
            total = qty.required_qty * self.quantity
            qty.write({'required_qty': total})



                # raise UserError('It have less quantity')

    def confirm_mrp(self):
        if self.bom_id:
            self.write({'state': 'confirmed'})

        else:
            raise UserError('The BOM does not exist')

    def start_production(self):
        if self.is_available:
            self.write({'state': 'in_progress'})
        else:
            raise UserError('The products not fully available')

    def done_mrp(self):
        for qty in self.material_line_ids:
            if qty.consumed_qty == 0:
                raise UserError('all product not consumed')
            # self.write({'state': 'done'})
        else:
            self.write({'state': 'done'})

    def cancel_mrp(self):
        self.write({'state': 'cancel'})

    def consume_mrp(self):
        for qty in self.material_line_ids:
            if qty.consumed_qty:
                raise UserError('This already consumed')
            qty.write({'consumed_qty': qty.required_qty})
            self.onchange_material_line_ids()
            if qty.consumed_qty > qty.required_qty:
                raise UserError('Consumed products are high')

    def write(self, vals):
        res = super().write(vals)
        total = 0
        for qty in self.material_line_ids:
            total = total + qty.required_qty
        return res

    def action_consumed_products(self):
        self.ensure_one()
        consume = self.env['mrp.production.material.line'].search([
            ('production_id', '=', self.id),
        ])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Consume',
            'res_model': 'mrp.production.material.line',
            "domain": [('production_id', 'in', self.id)],
            'res_id': consume.ids,
            'view_mode': 'list',
            'target': 'current',
        }

    @api.onchange('material_line_ids')
    def onchange_material_line_ids(self):
        total = 0
        for qty in self.material_line_ids:
            total = total + qty.required_qty
            if qty.required_qty and qty.consumed_qty:
                remaining = qty.available_qty - qty.consumed_qty
                if remaining < 0:
                    raise UserError('Remaining qty is negative')
                qty.write({'remaining_qty': remaining})
        self.write({
            'consumed_products': total,
            'state': 'done',
        })
        for qty in self.material_line_ids:
            print(1)

            if qty.required_qty > qty.product_id.qty_available:
                print(2)
                self.write({'is_available':False})
                break

            elif qty.required_qty == qty.product_id.qty_available:
                self.write({'is_available': True})
            else:
                print(3)
                self.write({'is_available':True})
        # for qty in self.material_line_ids:
        #     if qty.required_qty > qty.available_qty:

    def partially_produce(self):
        # produce = 0
        quantity = 0
        l_qty = []
        for qty in self.material_line_ids:
            produce = 0
            bom_product = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', self.product_id.id),
            ], limit=1)
            for q in bom_product.bom_line_ids:
                quantity = quantity + q.product_qty
                if q.product_qty < qty.required_qty:
                    produce = produce + 1
            l_qty.append(produce)

        min_qty = min(l_qty)
        self.write({'produced_qty': min_qty})
        manufacture =[]

        for q in self.bom_id.bom_line_ids:
            man = q.product_qty
            for i in range(min_qty-1):
                man += man

            manufacture.append(man)
            for index,value in enumerate(manufacture):
                self.material_line_ids[index].write({
                    'consumed_qty': value,
                    'remaining_qty': self.material_line_ids[index].available_qty - value,
                })
        print(manufacture)