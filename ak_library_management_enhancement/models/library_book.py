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
