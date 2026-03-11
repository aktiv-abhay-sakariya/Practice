# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class LibraryBook(models.Model):
    _inherit = ['library.book', 'mail.thread', 'mail.activity.mixin']

    image = fields.Image(string='Book Image')
    publication_date = fields.Date(
        string='Date of Publication',
        required=True,
        tracking=True
    )

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
    
    def create_message(self):
        self.message_post(
            body=f"this is custome message",
            message_type='comment',
        )
    
    def create_activity(self):
        self.activity_schedule(
            'mail.mail_activity_data_email',
            user_id=self.env.user.id,
            note="Reminder to follow up",
            date_deadline=fields.Date.today()
        )
