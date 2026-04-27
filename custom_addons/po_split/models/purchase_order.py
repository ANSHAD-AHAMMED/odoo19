from odoo import api, models, fields, _, exceptions
from collections import defaultdict


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    split_order_ids = fields.Many2many(
        comodel_name="purchase.order",
        relation="purchase_order_split_rel",
        column1="original_order_id",
        column2="split_order_id",
        string="Split Orders",
        copy=False,
        readonly=True,
    )

    split_order_count = fields.Integer(
        string="Split Order Count",
        compute="_compute_split_order_count",
    )

    is_split_order = fields.Boolean(
        string="Is Split Order",
        default=False,
        copy=False,
        readonly=True,
    )

    original_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Original Order",
        copy=False,
        readonly=True,
    )

    @api.depends("split_order_ids")
    def _compute_split_order_count(self):
        print('self=',self)
        for record in self:
            record.split_order_count = len(record.split_order_ids)
            print('record=', record)

    def action_view_split_orders(self):
        self.ensure_one()
        return {
            "name": _("Split Purchase Orders"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "list,form",
            "domain": [("id", "in", self.split_order_ids.ids)],
            "context": {"create": False},
        }

    def action_view_original_order(self):
        self.ensure_one()
        return {
            "name": _("Original Purchase Order"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": self.original_order_id.id,
        }

    def _get_lowest_price_vendor(self, product, quantity=1, currency=None):
        if not product:
            return 0.0

        currency = currency or self.env.company.currency_id

        supplierinfo_records = self.env["product.supplierinfo"].search([
            ("product_tmpl_id", "=", product.product_tmpl_id.id),
            "|",
            ("product_id", "=", False),
            ("product_id", "=", product.id),
        ])

        if not supplierinfo_records:
            return None, 0.0

        best_vendor = None
        best_price = None

        for info in supplierinfo_records:
            if info.min_qty > quantity:
                continue

            price = info.price

            if info.currency_id and info.currency_id != currency:
                price = info.currency_id._convert(
                    price,
                    currency,
                    self.env.company,
                    fields.Date.today(),
                )

            if best_price is None or price < best_price:
                best_price = price
                best_vendor = info.partner_id

        return best_vendor, best_price or 0.0

    def _build_vendor_line_map(self):
        vendor_map = defaultdict(list)
        for line in self.order_line:
            vendor, _price = self._get_lowest_price_vendor(
                line.product_id,
                quantity=line.product_qty,
            )

            vendor_map[vendor].append(line)

        return vendor_map

    def _create_split_order_for_vendor(self, vendor, lines):
        self.ensure_one()
        new_order = self.env["purchase.order"].create({
            "partner_id": vendor.id,
            "currency_id": self.currency_id.id,
            "date_order": self.date_order,
            "date_planned": self.date_planned,
            "company_id": self.company_id.id,
            "picking_type_id": self.picking_type_id.id,
                                                                                                                                                                                "dest_address_id": self.dest_address_id.id if self.dest_address_id else False,
            "note": self.note,
            "is_split_order": True,
            "original_order_id": self.id,
            "origin": self.name,
        })

        for line in lines:
            supplierinfo = self.env["product.supplierinfo"].search([
                ("partner_id", "=", vendor.id),
                ("product_tmpl_id", "=", line.product_id.product_tmpl_id.id),
                "|",
                ("product_id", "=", False),
                ("product_id", "=", line.product_id.id),
            ], limit = 1)

            self.env["purchase.order.line"].create({
                "order_id": new_order.id,
                "product_id": line.product_id.id,
                "name": line.name,
                "product_qty": line.product_qty,
                "product_uom_id": line.product_uom_id.id,
                "price_unit": supplierinfo.price if supplierinfo else line.price_unit,
                "date_planned": line.date_planned,
                "tax_ids": [(6, 0, line.tax_ids.ids)],  
                "analytic_distribution": line.analytic_distribution or {},
            })

        return new_order

    def button_confirm(self):
        orders_to_confirm_normally = (
            self.env["purchase.order"]
        )

        for order in self:
            if order.is_split_order or not order.order_line:
                orders_to_confirm_normally |= order
                continue

            vendor_map = order._build_vendor_line_map()

            if len(vendor_map) <= 1:
                orders_to_confirm_normally |= order
                continue

            split_orders = self.env["purchase.order"]

            for vendor, lines in vendor_map.items():
                if vendor is None:
                    continue

                split_orders |= order._create_split_order_for_vendor(vendor, lines)

            if split_orders:
                order.split_order_ids = [(6, 0, split_orders.ids)]
                split_orders.button_confirm()
                order.write({"state": "cancel"})
                order.message_post(
                    body=_(
                        "This order was automatically split into %(count)s "
                        "vendor-specific POs upon confirmation: %(names)s",
                        count=len(split_orders),
                        names=", ".join(split_orders.mapped("name")),
                    )
                )
            else:
                orders_to_confirm_normally |= order

        if orders_to_confirm_normally:
            return super(PurchaseOrder, orders_to_confirm_normally).button_confirm()

        return True

