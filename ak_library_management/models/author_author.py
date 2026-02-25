# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Author(models.Model):
    _name = 'author.author'
    _description = "Authors"

    name = fields.Char(string = "Author name", required = True)
    dob_date = fields.Date(string = "Date of Birth", required = True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string = "Gender",
        default='male',
        required=True
    )
    nationality = fields.Char(string = "Nationality", required = True)
    email = fields.Char(string = "Email", required = True)
    phone = fields.Char(string = "Phone No", required = True)
    social_profile = fields.Char(string = "Social Profile", required = True)
    book_ids = fields.One2many(
        comodel_name = 'author.book',
        inverse_name = 'author_id',
        string = 'Books',
    )
