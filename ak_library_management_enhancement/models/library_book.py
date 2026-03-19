# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class LibraryBook(models.Model):
    _inherit = ['library.book', 'mail.thread', 'mail.activity.mixin']

    image = fields.Image(string='Book Image')
