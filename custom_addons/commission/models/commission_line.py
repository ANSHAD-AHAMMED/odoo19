# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CommissionLine(models.Model):
    _name = 'commission.line'
    _description = 'Commission Line'

    sale_order_id = fields.Many2one('sale.order', string='Sales Order')
    sales_person_id = fields.Many2one('res.users', string="Sales Person")
    commission_percentage = fields.Float(string="Commission Percentage", related="sales_person_id.sale_commission_percentage")
    commission_percentage_amount = fields.Float(
        string="Percentage",
        compute='_compute_commission_percentage_amount',
        store=True
    )
    product_price = fields.Float(string="Product Price")
    product_id= fields.Many2one('product.product', string="Product")

    @api.depends('commission_percentage')
    def _compute_commission_percentage_amount(self):
        for order in self:
            order.commission_percentage_amount = order.product_price * (order.commission_percentage / 100)