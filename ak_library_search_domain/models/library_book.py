# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LibraryBook(models.Model):
    _inherit = 'library.book'
    
    total_products = fields.Integer(
        string = "Products",
        compute="_compute_product_count"
    )
    
    @api.depends('is_product_created')
    def _compute_product_count(self):
        """
        Count the total product variants of the book.
        """
        self.total_products = self.env['product.product'].search_count([
            ('book_id','=',self.id)
        ])
