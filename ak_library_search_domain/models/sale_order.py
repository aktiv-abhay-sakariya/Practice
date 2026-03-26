# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_book_added = fields.Boolean(string="Book Added")

    def action_open_add_book_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Books',
            'res_model': 'sale.book.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_id': self.id
            }
        }

    def action_open_edit_book_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Books',
            'res_model': 'sale.book.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_id': self.id,
                'edit_mode': True
            }
        }