# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_book_product = fields.Boolean(string = 'book product')
    book_id = fields.Many2one(
        comodel_name='library.book',
        string = 'book product',
    )
    total_books = fields.Integer(
        string="Books",
        compute="_compute_books_count"
    )

    def action_open_book_view(self):
        """
        Redirect to the of the related library.book form view.
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'res_id': self.book_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.depends('book_id')
    def _compute_books_count(self):
        """
        Count the total books of the product.
        """
        self.total_books = len(self.book_id)
