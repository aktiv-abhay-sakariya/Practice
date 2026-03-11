# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_book_product = fields.Boolean(string = 'book product', default = False)
    book_id = fields.Many2one(
        comodel_name='library.book',
        string = 'book product',
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
            'context': {'active_id': self.id},
            'target': 'current',
        }