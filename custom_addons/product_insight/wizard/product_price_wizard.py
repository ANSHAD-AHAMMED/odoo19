# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductPriceWizard(models.TransientModel):
    _name = 'product.price.wizard'
    _description = 'Product Product Wizard'

    new_price = fields.Float(string="New Price")

    product_ids = fields.Many2many(
        'product.product',
        string="Product"
    )

    same_price_product_ids = fields.Many2many(
        'product.product',
        string="Same Price",
        compute="_compute_same_price_product",
        readonly=True,
    )

    vendor_ids = fields.Many2many(
        'product.supplierinfo',
        string="Vendor",
        compute="_compute_vendors",
        readonly=True,
    )

    @api.depends_context('product_id')
    def _compute_same_price_product(self):
        """ find product with same price """
        for wizard in self:
            product = self.env['product.product'].browse(
                self.env.context.get('product_id')
            )

            if product:
                wizard.same_price_product_ids = self.env['product.product'].search([
                    ('list_price','=',product.list_price),
                    ('id','!=',product.id)
                ])
            else:
                wizard.same_price_product_ids = False

    @api.depends_context('product_id')
    def _compute_vendors(self):
        """ find the vendors of the product """
        for wizard in self:
            product = self.env['product.product'].browse(
                self.env.context.get('product_id')
            )
            wizard.vendor_ids = product.seller_ids

    def action_confirm(self):
        """ confirm the price """
        for product in self.product_ids:
            product.list_price = self.new_price

            product = self.env['product.product'].search([])
            print("All Products:", product.mapped('name'))

            premium_products = product.filtered(lambda p: p.list_price > 1000)
            print("Premium Products:", premium_products.mapped('name'))