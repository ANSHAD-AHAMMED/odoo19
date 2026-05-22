# -*- coding: utf-8 -*-
from odoo import  models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def pricelist_selection(self):

        """ Select pricelist based on customer's country """
        price_lists = self.env['country.pricelist'].search([
            ('country_id', '=', self.partner_id.country_id),
        ],limit=1)

        if price_lists:
            self.write({
                'pricelist_id': price_lists.pricelist_id,
            })
