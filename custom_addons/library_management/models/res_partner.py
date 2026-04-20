# -*- coding: utf-8 -*-
from odoo import fields, models, _, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    checkout_ids = fields.One2many(
        'library.checkout', 'partner_id',
        domain=[
            '|','|',
            ('state', '=', 'check_out'),
            ('state', '=', 'returned'),
            ('state', '=', 'over_due'),
        ])

    # checkout_line_ids = fields.One2many('library.checkout.line', 'partner_id',)
    borrow_limit = fields.Integer(string="Borrow Limit", default=1)
    late_count = fields.Integer(compute="_compute_late_count", store=True)
    books = fields.Integer(string="Borrowed books", compute="_compute_book_count", store=True)

    total_penalty = fields.Float(compute="_compute_late_count", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ Add the books borrow limit when create new partner """
        print("vals_list=",vals_list)
        limit_param = self.env['ir.config_parameter'].sudo().get_param(
            'library_management.maximum_borrow_books'
        )
        print('maximum_borrow_books=',limit_param)

        limit = int(limit_param) if limit_param else 0

        for vals in vals_list:
            print('borrow limit=',self.borrow_limit)
            if 'borrow_limit' in vals:
                print('hi')
            # print("vals=",vals)
            # print("borrow_limit=",type(self.borrow_limit))
            # print("limit=",type(limit))
                vals['borrow_limit'] = limit
                print("vals=",vals['borrow_limit'])
        return super().create(vals_list)

    def action_late_return_details(self):
        """ Checkout late return details of customers """
        for partner in self:
            checkouts = self.env['library.checkout'].search([
                ('partner_id', '=', partner.id),
                ('is_late', '=', True),
            ])
            partner.late_count = len(checkouts)
            partner.total_penalty = sum(checkouts.mapped('penalty'))
            print('partner.late_count=', partner.late_count)
            print('partner.total_penalty=', partner.total_penalty)

        self.ensure_one()
        return {
            "name": "Late Returns",
            "type": "ir.actions.act_window",
            "res_model": "library.checkout",
            "view_mode": 'list,form',
            "domain": [
                ('partner_id', '=', self.ids),
                ('is_late', '=', True),
            ],
            "target": "current",
        }

    def _compute_late_count(self):
        """ Compute late count and penalty of customers """
        for partner in self:
            checkouts = self.env['library.checkout'].search([
                ('partner_id', '=', partner.id),
                ('is_late', '=', True),
            ])
            partner.late_count = len(checkouts)
            partner.total_penalty = sum(checkouts.mapped('penalty'))

    def action_checkout_details(self):
        """ borrowed book details """
        for partner in self:
            books = self.env['library.checkout.line'].search([
                ('partner_id', '=', partner.id),
            ])
            partner.books = len(books)
            print("book.books=",partner.books)

        self.ensure_one()

        return {
            "name": "Borrowed Books",
            "type": "ir.actions.act_window",
            "res_model": "library.checkout.line",
            "view_mode": "list,form",
            "domain": [
                ('checkout_id.partner_id', '=', self.id),
            ],
            "target": "current",
        }


    def _compute_book_count(self):
        """ borrowed book count """
        for book in self:
            books = self.env['library.checkout.line'].search([
                ('book_id', '=', book.id),
            ])
            book.books = len(books)