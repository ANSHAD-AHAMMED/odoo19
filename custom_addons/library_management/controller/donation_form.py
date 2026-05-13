# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request


class DonationForm(http.Controller):

    @http.route('/website/book/form', type='http', auth='public', website=True)
    def donation_form(self, **kw):
        """ Render the book donation form """
        print('start')
        genre = request.env['library.genre'].sudo().search([])
        return request.render('library_management.book_donation_form_template',{
            'genre': genre,
        })

    @http.route('/website/book/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def donation_create(self, **post):
        """ Handle form submission and create a new book """

        print('controller')
        name = post.get('name')
        author_id = post.get('author_id')
        isbn = post.get('isbn')
        genre_id = post.get('genre_id')
        cover_image = post.get('cover_image')
        condition = post.get('condition')

        if not name:
            print('no name')
            # If name is missing, redirect back to form with an error message
            return request.render('library_management.book_donation_form_template', {
                'error': 'Name is required!'
            })

        if author_id:
            author = request.env['library.author'].sudo().search([
                ('name', '=', author_id)
            ])
            if not author:
                author = request.env['library.author'].sudo().create({
                    'name': author_id,
                })

        if cover_image:

            data = cover_image.read()
            decoded = base64.b64encode(data)
        else:
            decoded = None

        new_book = request.env['library.book'].sudo().create({
            'name': name,
            'author_id': author.id if author_id else None,
            'genre_id': genre_id,
            'isbn': isbn,
            'price': 0,
            'cost': 0,
            'cover_image': decoded,
            'status': 'coming_soon',
            'condition': condition,
        })
        print('create done')

        return request.render('library_management.portal_my_home_book_donation_form_views',{
            'view_book': new_book,
        })

