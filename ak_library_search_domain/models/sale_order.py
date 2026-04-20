# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    is_book_add = fields.Boolean()

    def action_add_edit_book_line(self):
        """
        Opens a wizard to add a book or edit the existing book quantity to the 
        current sale order line.

        Args:
            self: An instance of the current model.

        Return : 
            dict :A dictionary representing the window action for the wizard.
        """
        rtn = {
            'type': 'ir.actions.act_window',
            'res_model': 'book.order.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
        if self.is_book_add:
            rtn['name'] = 'Edit book product'
            rtn['context'] = {'edit_line': True}
        else:
            rtn['name'] = 'Add book product'
        return rtn
