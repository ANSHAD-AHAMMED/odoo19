# -*- coding: utf-8 -*-
from odoo import fields, models, api

class BulkProduct(models.Model):
    _name = 'bulk.product'
    _description = 'Bulk Product'

    product_id = fields.Many2one('product.product', string="Products")
    product_uom_qty = fields.Float(string="Quantity")
    sale_order_id = fields.Many2one('sale.order', string="Sales Order")

    # product_id = fields.Many2one(
    #     string="Product Template",
    #     comodel_name='product.template',
    #     # compute='_compute_product_template_id',
    #     readonly=False,
    #     # search='_search_product_template_id',
    #     # domain=lambda self: self.env['sale.order.line']._fields['product_id']._description_domain(self.env),
    # )

    # domain=lambda self: self._fields['product_id']._description_domain(self.env),
    # )

    # product_uom_qty = fields.Float(
    #     string="Quantity",
    #     # compute='_compute_product_uom_qty',
    #     digits='Product Unit', default=1.0,
    #     # store=True, readonly=False, required=True, precompute=True
    # )

    # display_type = fields.Selection(
    #     selection=[
    #         ('line_section', "Section"),
    #         ('line_subsection', "Subsection"),
    #         ('line_note', "Note"),
    #     ],
    #     default=False)

    # @api.depends('product_id')
    # def _compute_product_template_id(self):
    #     for line in self:
    #         line.product_template_id = line.product_id.product_tmpl_id
    #
    # def _search_product_template_id(self, operator, value):
    #     return [('product_id.product_tmpl_id', operator, value)]
    #
    # @api.depends('display_type', 'product_id')
    # def _compute_product_uom_qty(self):
    #     for line in self:
    #         if line.display_type:
    #             line.product_uom_qty = 0.0
