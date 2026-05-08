# -*- coding: utf-8 -*-
from odoo import api, fields, models

class LibraryBookImage(models.Model):
    _name = 'library.book.image'
    _description = 'Library Book Image'

    book_image = fields.Binary(string='Book Image')