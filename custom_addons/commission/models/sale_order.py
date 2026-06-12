# -*- coding: utf-8 -*-
from odoo import api, fields, models, Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    commission_line_ids = fields.One2many(
        "commission.line",
        "sale_order_id",
        string="Commission Lines",
    )
    order_line = fields.One2many('sale.order.line', 'order_id', string="Order Lines")
    user_id = fields.Many2one('res.users', string="User")
    approver_id = fields.Many2one('res.users', string="Approver", store=True, readonly=True)
    preparer_id = fields.Many2one('res.users', string="Preparer", store=True, readonly=True)
    @api.onchange('order_line')
    def sale_commission(self):
        """ Add products and salesman into commission lines """
        for order in self:

            if order.partner_id and not (order._origin.id and order.user_id):
                order.user_id = (
                    order.partner_id.user_id
                    or order.partner_id.commercial_partner_id.user_id
                    or (self.env.user.has_group('sales_team.group_sale_salesman') and self.env.user)
                )
            order.write({'commission_line_ids': [Command.clear()]})
            new_lines = self.env['commission.line']

            for product in order.order_line:
                new_line = self.env['commission.line'].new({
                    'product_id': product.product_id.id,
                    'product_price': product.price_subtotal,
                    'sales_person_id':order.user_id.id,
                })
                new_lines |= new_line
            order.commission_line_ids |= new_lines

    def commission_preparation(self):
        """ Commission Preparation Button """
        if self.user_id:
            self.preparer_id = self.env.user

    def commission_approval(self):
        """ Commission Approval Button """
        if self.user_id:
            self.approver_id = self.env.user

