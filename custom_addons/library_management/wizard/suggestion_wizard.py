# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SuggestionWizard(models.TransientModel):
    _name = 'suggestion.wizard'
    _description = 'Suggestion Wizard'

    recommended_book_ids = fields.Many2many('library.book', string="Recommended Books")

    @api.model
    def default_get(self, fields_list):
        """ Automatically filter the wizard based on the authors, genres and most borrowed books. """
        res = super().default_get(fields_list)

        book_ids = self.env.context.get('default_book_id')
        print(book_ids)

        if book_ids:
            books = self.env['library.book'].browse(book_ids)
            top_books = self.env['library.book'].search([], order='count desc', limit=10)
            max_popular_count = max(top_books.mapped('count')) if top_books else 0


            recommended_books = self.env['library.book'].search([
                ('id', 'not in', books.ids),
                ('status', '!=', 'unavailable'),
                '|', '|',
                ('author_id', 'in', books.mapped('author_id')),
                ('genre_id', 'in', books.mapped('genre_id')),
                ('count', '=', max_popular_count)
            ])

            res['recommended_book_ids'] = [fields.Command.set(recommended_books.ids)]
        return res


    def action_apply(self):
        """ To add the books from wizard to checkout_line_ids """
        checkout_id = self.env.context.get('checkout_id')
        print(checkout_id)

        if not checkout_id:
            return

        checkout = self.env['library.checkout'].browse(checkout_id)
        lines = [(4, book.id) for book in self.recommended_book_ids]

        checkout.write({
            'checkout_line_ids': lines
        })
