from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_month_discount_total(self):
        """ Start date and end date """
        today = fields.Date.today()
        start_date = today.replace(day=1)

        end_date = today.replace(month=today.month + 1, day=1)

        partner = self.order_id.partner_id
        if not partner:
            return 0

        lines = self.search([
            ('id', '!=', self.id),
            ('create_date', '>=', start_date),
            ('create_date', '<', end_date),
            ('order_id.state', 'in', ['sale', 'done']),
            ('order_id.partner_id', '=', partner.id),
            ('company_id', '=', self.env.company.id),
        ])

        total = 0
        for line in lines:
            total += line._get_discount_amount()

        return total

    # @api.depends('discount', 'product_uom_qty', 'price_unit')
    def _get_discount_amount(self):
        """ Change all type of discount into amount """
        self.ensure_one()

        if self.discount:
            return self.price_unit * self.product_uom_qty * (self.discount / 100)

        return 0


    @api.onchange('discount', 'product_uom_qty', 'price_unit')
    def _onchange_discount_limit(self):
        """ Warning message when discount limit exceeded """
        limit = float(self.env['ir.config_parameter'].sudo().get_param(
            'sale_discount_limit.discount_limit', default=0
        ))

        for record in self:
            current_total = record._get_month_discount_total()
            print('current_total=', current_total)
            current_line_discount = record._get_discount_amount()
            print('current_line_discount=', current_line_discount)

            if current_total + current_line_discount > limit:
                return {
                    'warning': {
                        'title': "Discount Limit Exceeded",
                        'message': "Monthly discount limit exceeded!",
                    }
                }
