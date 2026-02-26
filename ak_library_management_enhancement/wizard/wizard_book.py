# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Author(models.TransientModel):
    _name = "book.author.wizard"

    author_id = fields.Many2one('author.author', string='Author')


    def action_done(self):
        active_id = self.env.context.get('active_id')
        book = self.env['library.book'].browse(active_id)
        book.author_id = self.author_id.id
        return {'type': 'ir.actions.act_window_close'}
