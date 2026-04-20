# -*- coding: utf-8 -*-

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('name', 'city', 'phone')
    def _compute_display_name(self):
        """
        Compute the display name for each record by concatenating the name, 
        city, and phone number in many-to-one dropdown results.
        
        Return : None
        """
        for rec in self:
            rec.display_name = f'{rec.name} - {rec.city} - {rec.phone}'

    def action_view_book_reservation(self):
        """
        Opens a book reservation list,form view to show the current customer
        reserved books.
        
        Return : 
            dict :A dictionary representing the window action for the 
            list and form view.
        """
        return {
            'name': 'Book Reservation',
            'type': 'ir.actions.act_window',
            'res_model': 'book.reservation',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'is_customer_view': True}
        }
