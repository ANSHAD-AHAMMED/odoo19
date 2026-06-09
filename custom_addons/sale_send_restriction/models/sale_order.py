# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_send(self):
        if not self.order_line:
            raise UserError('sale order line is empty')

        return super().action_quotation_send()