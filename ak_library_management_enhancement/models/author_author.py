# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Author(models.Model):
    _inherit = 'author.author'

    total_book = fields.Integer(string='Total Book')

    status = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked')
    ],
        string = "status",
        default='new',
    )

    @api.onchange('book_ids')
    def book_info(self):
        self.total_book = self.env['library.book'].search_count([('author_id', '=', self.id)])