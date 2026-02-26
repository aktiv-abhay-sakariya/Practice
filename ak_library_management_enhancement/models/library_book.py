# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class LibraryBook(models.Model):
    _inherit = 'library.book'

    image = fields.Image(string='Book Image')
    sequence = fields.Char(string='Sequence Number', store=True, default='New')


    @api.model_create_multi
    def create(self, vals):
        """Create a new record with the given values."""
        for val in vals:
            if val.get('sequence', 'New') == 'New':
                rec_date = val.get('publication_date')
                sequence_number = self.env['ir.sequence'].next_by_code(
                    'library.book', sequence_date=rec_date)
                val['sequence'] = sequence_number
        return super(LibraryBook, self).create(vals)

    def find_book(self):
        for rec in self:
            record = rec.search([('price', '>', '200')])
            print(record)

    def find_book_count(self):
        book_count = 0
        for rec in self:
            book_count = book_count + rec.search_count([('price', '>', '200')])
            print(book_count)

    def action_done_show_wizard(self):
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'book.author.wizard',
           'target': 'new',
           'view_mode': 'form',
           'context': {'active_id': self.id},
        }
