# -*- coding: utf-8 -*-
from odoo import fields, models, api

class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"

    name = fields.Char(string="Author")
    description = fields.Char(string="Description")

    book_ids = fields.One2many('library.book', 'author_id', string="Books")

