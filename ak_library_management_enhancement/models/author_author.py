# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Author(models.Model):
    _name = 'author.author'
    _inherit = ['author.author', 'mail.thread', 'mail.activity.mixin']

    total_book = fields.Integer(string='Total Book')
    author_status = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked')
    ],
        string = "status",
        default='new',
    )
