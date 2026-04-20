# -*- coding: utf-8 -*-
from odoo import fields, models

class LibraryGenre(models.Model):
    _name = 'library.genre'
    _description = 'Genre'

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")

    book_ids = fields.One2many('library.book','genre_id', string="Author")