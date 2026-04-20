# -*- coding: utf-8 -*-
from odoo import api, fields, models

class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Library Publisher'

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")

    book_ids = fields.One2many('library.book', 'publisher_id', string="Books")