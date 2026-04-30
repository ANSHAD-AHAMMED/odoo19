from odoo import api, models, fields, _
from collections import defaultdict


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    split_order_ids = fields.Many2many(
        comodel_name="purchase.order",
        relation="purchase_order_split_rel",
        column1="original_order_id",
        column2="split_order_id",
        string="Split Orders",
    )

    split_order_count = fields.Integer(
        string="Split Order Count",
        compute="_compute_split_order_count",
    )

    is_split_order = fields.Boolean(
        string="Is Split Order",
        default=False,
    )

    original_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Original Order",
    )

    @api.depends("split_order_ids")
    def _compute_split_order_count(self):
        """ count how many split orders """
        print('1')
        print('split_order_ids=',self.split_order_ids)
        for record in self:
            record.split_order_count = len(record.split_order_ids)
            print('split_order_count=', record.split_order_count)

    def _create_split_order_for_vendor(self, vendor, lines):
        """ Create purchase order for each vendor """
        print('4')
        self.ensure_one()
        new_order = self.env["purchase.order"].create({
            "partner_id": vendor.id,
            "date_order": self.date_order,
            "date_planned": self.date_planned,
            "company_id": self.company_id.id,

            "is_split_order": True,
            "original_order_id": self.id,
        })

        product_qty_map = {}

        for line in lines:
            product_id = line.product_id.id

            if product_id not in product_qty_map:
                product_qty_map[product_id] = {
                    'qty':0,
                    'line':line,
                }
            key = line.product_id.id
            product_qty_map[key]['qty'] += line.product_qty
            product_qty_map[key]['line'] = line
            print('line=', line.product_id.name)
            print('product_qty_map=', product_qty_map)
            # product = line.product_id
            # if not line.product_id in lines:
            #     print('hi')
            # existing_line = line.filtered(lambda l: l.product_id.id == line.product.id)
            # print('existing_line=', existing_line)
            #
            # if existing_line:
            #     print('a')
            #     existing_line.order_line.product_qty += line.product_qty
            #
            # else:
        for product_id, data in product_qty_map.items():
            print('b')
            line = data["line"]
            print('data=',data['qty'])
            print('date_planned=',line.date_planned)
            self.env["purchase.order.line"].create({
                "order_id": new_order.id,
                "product_id": product_id,
                "product_qty": data['qty'],
                "date_planned": line.date_planned,
            })
                # print('new_line=', new_line)

        return new_order

    def _get_lowest_price_vendor(self, product):
        """ find lowest price vendor """
        print('2')
        print('product=', product)
        supplierinfo_records = self.env["product.supplierinfo"].search([
            ("product_tmpl_id", "=", product.product_tmpl_id.id),
            ("product_id", "=", False),
        ])

        lowest_vendor = None
        lowest_price = None

        for info in supplierinfo_records:

            price = info.price
            print('price=', price)

            if lowest_price is None or price < lowest_price:
                lowest_price = price
                lowest_vendor = info.partner_id

        return lowest_vendor, lowest_price

    def _build_vendor_line_map(self):
        """ group vendor and product lines"""
        print('3')
        vendor_map = defaultdict(list) # Automatically create list for each vendor
        for line in self.order_line:
            vendor,price = self._get_lowest_price_vendor(line.product_id,)

            vendor_map[vendor].append(line)

        return vendor_map

    def button_confirm(self):
        print('5')
        confirm_normally = self.env["purchase.order"]


        for order in self:
            vendor_map = order._build_vendor_line_map()
            print('vendor_map=', vendor_map)

            if order.is_split_order or not order.order_line or len(vendor_map) <= 1:
                print('suuuuiii')
                confirm_normally |= order ###
                continue

            split_orders = self.env["purchase.order"]
            print('hellllo')

            for vendor, lines in vendor_map.items():
                print('abc')
                split_orders |= order._create_split_order_for_vendor(vendor, lines)
                print('vendor=', vendor)
                print('lines=', lines)
                print('split_orders=', split_orders)

            if split_orders:
                order.split_order_ids = [(6, 0, split_orders.ids)]
                order.write({"state": "cancel"})
            else:
                confirm_normally |= order

        if confirm_normally:
            return super().button_confirm()

        return True

    def action_view_split_orders(self):
        """ open window for split orders """
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
        """ action to see original order """
        self.ensure_one()
        return {
            "name": _("Original Purchase Order"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": self.original_order_id.id,
        }
