# -*- coding: utf-8 -*-
from odoo import fields, models

class LibraryBookCondition(models.Model):
    _name = 'library.book.condition'
    _description = 'Library Book Condition'

    name = fields.Char(string="Name")

    book_ids = fields.One2many('library.book','condition_id', string="Author")