# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book'

    author_id = fields.Many2one('library.author', string="Author")
    publisher_id = fields.Many2one('library.publisher', string="Publisher")
    genre_id = fields.Many2one('library.genre', string="Genre")
    product_id = fields.Many2one('product.product', string='Product')
    condition_id = fields.Many2one('library.book.condition', string="Condition")

    checkout_ids = fields.One2many('library.checkout', 'book_id')
    tag_ids = fields.Many2many('library.tag', string="Tags")

    cover_image = fields.Image()

    sequence_number = fields.Char(string="Reference Number", default=lambda self: _('New'), readonly=True, copy=False, help="Reference Number of the book")
    name = fields.Char(string="Book Name", required=True)
    isbn = fields.Char(string="ISBN", required=True)

    count = fields.Integer(string="Book Count")

    price = fields.Float(string="Price", required=True)
    cost = fields.Float(string="Cost", required=True)

    publish_date = fields.Datetime(string="Publish Date")

    book_image_ids = fields.Many2many(
        comodel_name="library.book.image",
        string="Book Image",
    )

    status = fields.Selection(
        string="Status",
        selection=[
            ('coming_soon', 'Coming Soon'),
            ('available', 'Available'),
            ('unavailable', 'Unavailable')
        ],
    )

    condition = fields.Selection(
        string="Condition",
        selection=[
            ('new', 'New'),
            ('medium', 'Medium'),
            ('old', 'Old')
        ],
    )

    @api.constrains("isbn")
    def check_unique_isbn(self):
        """ Check if ISBN is unique or not"""
        for record in self:
            exist = self.search([
                ('isbn', '=', record.isbn),
                ('id', '!=', record.id),
            ])
            if exist:
                raise ValidationError("ISBN already exists")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a new book """
        category = self.env['product.category']
        book_category = category.search([('name', '=', 'Book')])

        if not book_category:
            book_category=category.create({'name': 'Book'})

        for vals in vals_list:
        # """Automatically generate a reference number for new books."""
            if vals.get('sequence_number', _("New")) == _("New"):
                vals['sequence_number'] = self.env['ir.sequence'].next_by_code('library.book')

            product = self.env['product.template'].create({
                'name': vals.get('name'),
                'type': 'consu',
                'list_price': vals.get('price'),
                'standard_price': vals.get('cost'),
                'categ_id': book_category.id,
            })

            vals['product_id'] = product.product_variant_id.id

        return super().create(vals_list)
