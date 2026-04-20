# -*- coding: utf-8 -*-
from ast import literal_eval

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    credit_limit_threshold = fields.Float(
        String='Credit Limit Threshold',
        config_parameter='credit_limit_restriction.credit_limit_threshold',
    )

    restricted_customer_tags = fields.Many2many(
        'res.partner.category',
        string="Restricted Customer Tags"
        # config_parameter='credit_limit_restriction.restricted_customer_tags',
    )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'credit_limit_restriction.restricted_customer_tags', self.restricted_customer_tags.ids)
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        restricted_customer_tags = with_user.get_param('credit_limit_restriction.restricted_customer_tags')
        res.update(restricted_customer_tags=[(6, 0, literal_eval(restricted_customer_tags))
                                             ] if restricted_customer_tags else False, )
        return res
