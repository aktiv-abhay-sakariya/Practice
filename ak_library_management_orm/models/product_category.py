# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    book_categ_id = fields.Many2one(
        comodel_name='book.category',
        string = 'book product',
    )

    def action_open_book_view(self):
        """
        Returns an action to open the related library book.
        """
        print('\n\n',self.book_categ_id == None)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'book.category',
            'res_id': self.book_categ_id.id,
            'view_mode': 'form',
            'context': {'active_id': self.id},
            'target': 'current',
        }