from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    justification = fields.Text(string="Justification")

    def button_confirm(self):
        """ Justification button """
        purchase = self.env["purchase.order"].search([
            ('partner_id', '=', self.partner_id),
            ('state', '=', 'purchase'),
        ],limit=1)
        if purchase:
            total = 0

            for order in purchase.order_line:
                total = order.price_unit
            value = self.order_line.price_unit - total
            percentage = value / 100

            if percentage >= 0.15:
                if not self.justification:
                    raise UserError('The amount difference is more than 15 %, justification needed')

        return super().button_confirm()


    def action_merge_duplicate_lines(self):

        self.ensure_one()

        if self.state not in ('draft', 'sent'):
            raise UserError(
                "Duplicate lines can only be merged while the order "
                "is in Draft or Quotation Sent state.")
        keeper = {}
        to_unlink = []

        for line in self.order_line:
            key = (
                line.product_id.id,
                # line.product_uom.id,
                line.price_unit,
                line.discount,
            )

            if key not in keeper:
                keeper[key] = line
            else:
                keeper[key].product_uom_qty += line.product_uom_qty
                to_unlink.append(line.id)

        if not to_unlink:
            raise UserError("No duplicate product lines found to merge.")

        self.env['sale.order.line'].browse(to_unlink).unlink()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Lines Merged"),
                'message': _(
                    "%d duplicate line(s) were consolidated successfully.",
                    len(to_unlink)
                ),
                'type': 'success',
                'sticky': False,
            },
        }
