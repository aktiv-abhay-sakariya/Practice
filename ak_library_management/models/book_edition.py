# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import  fields, models


class BookEdition(models.Model):
    _name = 'book.edition'
    _description = "Book Editions"

    name = fields.Char(string = "Edition", required = True)
    active = fields.Boolean(string = 'Active', default = True)
    quantity = fields.Integer(string = 'Quantity', required = True)
    book_price = fields.Float(string = 'Book Price', required = True)
