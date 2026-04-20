# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

class SalesOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def restricted_customer_with_tags(self):
        """ Restrict customer with tags and due amount"""
        with_user = self.env['ir.config_parameter'].sudo()
        restricted_customer_tag = with_user.get_param(
            'credit_limit_restriction.restricted_customer_tags','[]'
        )

        limit = float(self.env['ir.config_parameter'].sudo().get_param(
            'credit_limit_restriction.credit_limit_threshold', default=0
        ))
        print('limit=', limit)

        restricted_customer_tags = safe_eval(restricted_customer_tag)
        print('restricted_customer_tags=', restricted_customer_tags)

        customer_tags = self.partner_id.category_id.ids
        print('catgory_id=',customer_tags)

        common_tags = any(item in customer_tags for item in restricted_customer_tags)
        print('common_tags=', common_tags)

        over_limit = self.partner_id.credit > limit
        print('credit=',self.partner_id.credit)
        print('over_limit=', over_limit)

        if common_tags and over_limit:
            raise UserError("customer have reached the due limit also this customer have restricted tags")
        elif common_tags:
            raise UserError("this customer have restricted tags")
        elif over_limit:
            raise UserError("this customer have reached the due limit")

