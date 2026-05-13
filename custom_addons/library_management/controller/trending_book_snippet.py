# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import random
import string

class WebsiteProduct(http.Controller):

    @http.route('/get_product_categories', auth="public", type='jsonrpc',website=True)
    def get_product_category(self):
        """Get the website categories for the snippet."""
        top_books = self.env['library.book'].search([], order='count desc')

        trending_books = self.env[
           'library.book'].search_read([
           ('status','=','available'),
           ('count', '=', top_books)
        ])
        values = {
           'categories': trending_books,
        }
        return values

    @http.route('/random_number_generator', auth="public", type='jsonrpc', website=True)
    def random_number_generate(self):
        """ Generate a random string """
        length = 8
        dynamic_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        return dynamic_id

    @http.route('/slides/<int:book_id>', type='http', auth="user", website=True)
    def book_view(self, book_id=None):
        """ View book details that we donated """
        view_book = request.env['library.book'].sudo().browse(book_id)
        return request.render('library_management.portal_my_home_book_donation_form_views', {
           'view_book': view_book,
        })
