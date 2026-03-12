# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Author(models.Model):
    _name = 'author.author'
    _inherit = ['author.author', 'mail.thread', 'mail.activity.mixin']

    total_book = fields.Integer(string='Total Book', compute='_get_book_domain')
    author_status = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked')
    ],
        string = "status",
        default='new',
    )

    def _get_book_domain(self):
        self.total_book = self.env['library.book'].search_count([('author_id', '=', self.id)])

    def book_info(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'list,form',
            'domain': [('author_id', '=', self.id)],
            'context': {
                'default_author_id': self.id,
            },
            'target': 'current',
        }
