# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    date_today = fields.Datetime(string="Today", default=fields.Datetime.now)
    restrict_days = fields.Integer(string="Restrict Days", compute='_compute_restrict_days')
    last_price_update = fields.Datetime(string="Last Price Update")

    @api.onchange('list_price')
    def product_price_changing(self):
        """ Restrict Price Change if the condition not satisfied """
        for product in self:
            restrict_day = product._compute_restrict_days()

            products = self.env['sale.order.line'].search([
                ('state', '=', 'sale'),
                ('product_template_id', 'in', self._origin.id),
                ('order_id.date_order', '>', restrict_day),
            ]).mapped('price_unit')

            if products:
                avarage = sum(products)/len(products)

                if avarage > self.list_price:
                    raise UserError("price must be greater than avarage")

                elif not self.env.user.has_group('restrict_product_price.price_update_restriction_group'):
                    raise UserError("you have no access to change price")
                else:

                    price_update = fields.Datetime.now()
                    self.write({
                        'last_price_update': price_update,
                    })

    def _compute_restrict_days(self):
        """ Compute Restrict Days """
        if self.date_today:
            restrict_days = self.date_today - timedelta(days=30)
            return restrict_days

