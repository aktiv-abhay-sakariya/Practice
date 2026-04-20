# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    book_categ_id = fields.Many2one(
        comodel_name='book.category',
        string = 'book product',
    )
    total_book_categories = fields.Integer(
        string="Categories",
        compute="_compute_book_categories_count"
    )

    def action_open_book_category_view(self):
        """
        Redirect to the of the related book.category form view.
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'book.category',
            'res_id': self.book_categ_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.depends('book_categ_id')
    def _compute_book_categories_count(self):
        """
        Count the total book categories of the product category.
        """
        self.total_book_categories = len(self.book_categ_id)
