# -*- coding: utf-8 -*-
from odoo import models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """ Check the margin is reached or not. """
        failed_lines = []

        for order in self.order_line:
            if order.product_id.categ_id.minimum_margin_percent > 0:

                needed_margin = (order.product_id.categ_id.minimum_margin_percent / 100) * order.product_id.standard_price
                minimum_sale = needed_margin + order.product_id.standard_price

                if order.price_unit < minimum_sale:

                    failed_lines.append({
                        'name': order.product_id.name,
                        'minimum_sale': minimum_sale,
                    })

        if failed_lines:

            if not self.env.user.has_group('sale_order_margin.sale_order_margin_sales_administrator_group'):
                failed_line = [failed_line['name'] for failed_line in failed_lines]
                msg = _("Margin is not reached for product:%s", failed_line)
                order.order_id.sudo().message_post(body=msg)

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification','next': {
                            'type': 'ir.actions.act_window_close'
                        },
                    'params': {
                        'type': 'warning',
                        'title': _("Warning"),
                        'message': _(
                            f"Only Sales Administrator have permission for sale product less than minimum_margin_percent,\n"
                            f"{failed_line} have less than minimum_margin_percent\n"
                        ),
                    }
                }

            else:
                return super().action_confirm()

        return super().action_confirm()
