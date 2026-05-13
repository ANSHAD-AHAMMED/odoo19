# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class LibraryCustomPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        print('counters:', counters)
        print('self:', self)
        values = super()._prepare_home_portal_values(counters)
        if 'portal_donation' in counters:
            values['portal_donation'] = request.env[
                'library.book'].sudo().search_count([])
        return values

    @http.route(['/book_donation', '/book_donation/page/<int:page>'], type='http', auth="user", website=True)
    def portal_donation(self):
        """To search the donated books data in the portal"""

        donated_books = request.env['library.book'].sudo().search([
            ('create_uid', '=', request.env.user.user_id.id)])
        return request.render('library_management.portal_my_home_book_donation_views',
                              {
                                  'user_donations': donated_books,
                              })

    @http.route('/my/books/<int:book_id>', type='http', auth="user", website=True)
    def view_book(self, book_id=None):
        """ View book details that we donated """
        view_book = request.env['library.book'].sudo().browse(book_id)
        return request.render('library_management.portal_my_home_book_donation_form_views', {
            'view_book': view_book,
        })
