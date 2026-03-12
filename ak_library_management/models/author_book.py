# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AuthorBook(models.Model):
    _name = 'author.book'
    _description = "Author Books"

    book_id = fields.Many2one(
        comodel_name='library.book',
        string='Book',
        required=True
    )
    author_id = fields.Many2one(
        comodel_name='author.author',
        string='Author',
        ondelete='cascade',
    )
    isbn = fields.Char(string='ISBN Number', readonly=False)
    publication_date = fields.Date(
        string='Date of Publication',
        readonly=False
    )
    price = fields.Float(string='Book Price', readonly=False)
