# -*- coding: utf-8 -*-
from odoo import fields, models

class library_tag(models.Model):
    _name = "library.tag"
    _description = "Library Tag"

    name = fields.Char(string="Name")

    color = fields.Integer(string="Color")

    book_ids = fields.One2many('library.book', 'author_id', string="Books")
