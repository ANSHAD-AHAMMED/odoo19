from unicodedata import category

from odoo import fields, models, api

class AbinTask(models.Model):
    _name = 'abin.task'
    _description = 'Abin Task'

    partner_name = fields.Many2one('res.partner', string="Partner details")
    product_id = fields.Many2one('product.template', string="Product details")
    purchase_id = fields.Many2one('purchase.order', string="Order details")

    # NEW FIELDS

    # installment_amount = fields.Float(string="Installment Amount")
    # total_payable = fields.Float(string="Total Payable", compute="_compute_total_payable", store=True)

    def customer_details(self):
        for record in self:
            customer_name = record.partner_name.name
            email = record.partner_name.email
            phone = record.partner_name.phone
            city = record.partner_name.city
            company_name = record.product_id.parent_id.name

            print("customer name=",customer_name)
            print("phone =", phone)
            print("email =", email)
            print('city=',city)
            print('company=',company_name)

    # @api.onchange('loan_amount', 'installment_count')
    # def _onchange_installment(self):
    #     for rec in self:
    #         if rec.loan_amount and rec.installment_count:
    #             rec.installment_amount = rec.loan_amount / rec.installment_count
    #         else:
    #             rec.installment_amount = 0.0

    def product_details(self):
        for record in self:
            product = record.product_id.name
            category = record.product_id.categ_id.name
            sale_price = record.product_id.list_price
            cost_price = record.product_id.standard_price
            product_type = record.product_id.type

            print("product =", product)
            print("category =", category)
            print("sales price =", sale_price)
            print("cost_price =", cost_price)
            print("product_type =", product_type)

    # @api.depends('loan_amount')
    # def _compute_total_payable(self):
    #     for rec in self:
    #         rec.total_payable = rec.loan_amount

    def purchase_details(self):
        for record in self:
            vendor_name = record.purchase_id.partner_id.name
            vendor_id = record.purchase_id.partner_id.id
            vendor_country = record.purchase_id.partner_id.country_id.name
            vendor_currency = record.purchase_id.partner_id.currency_id.name
            all_purchase_orders = self.env['purchase.order'].search([
                ('partner_id', '=', vendor_name),
                ('state', 'in', ['purchase'])
            ])
            total_purchase_orders = len(all_purchase_orders)
            total_purchase_amount = sum(all_purchase_orders.mapped('amount_total'))

            purchase_order_line = self.env['purchase.order.line'].search([('order_id.partner_id', '=', vendor_id)])
            full_product = {}
            for i in purchase_order_line:
                product = i.product_id.name
                full_product[product] = full_product.get(product, 0) + i.product_uom_qty

            print("vendor_name =", vendor_name)
            print("vendor_country =", vendor_country)
            print("vendor_currency =", vendor_currency)
            print("total_purchase_orders =", total_purchase_orders)
            print("total_purchase_amount =", total_purchase_amount)
            print("products =", full_product)

