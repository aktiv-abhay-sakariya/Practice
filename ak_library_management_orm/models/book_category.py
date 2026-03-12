# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class BookCategory(models.Model):
    _inherit = 'book.category'

    product_categ_id = fields.One2many(
        comodel_name = 'product.category',
        inverse_name = 'book_categ_id',
    )

    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to prevent hierarchical loops.

        Args:
            vals (list): A list of dictionaries containing field values.

        Returns:
            recordset: The newly created book category records.
        """
        self._prevent_loop(vals)
        return super(BookCategory, self).create(vals)

    def write(self, vals):
        """
         Overrides the standard write method to prevent hierarchical loops 
        during updates.

        Args:
            vals (dict): A dictionary of fields and values being updated.

        Returns:
            bool: True if the record was updated successfully.
        """
        self._prevent_loop(vals)
        return super(BookCategory, self).write(vals)

    def _prevent_loop(self, vals):
        """
        Checks if a record update/create results in a parent-child loop.

        Args:
            vals (dict): Dictionary of field values to validate.
        """
        if 'parent_categ_id' in vals:
            if (self.id == vals['parent_categ_id'] or 
                self._check_category_loop(self.env['book.category'].search([
                    ('id','=',vals['parent_categ_id'])
                ]))):
                raise UserError('You cannot set a category as its own parent')

    def _check_category_loop(self, category):
        """
        Recursively checks if a given category is a parent of the current
        category.

        Args:
            category (recordset): The category record to check in the hierarchy.

        Returns:
            bool: True if a loop is detected, otherwise False.
        """
        while category:
            if category.id == self.id:
                return True
            category = category.parent_categ_id
        return False

    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)' to the name.

        Args:
            default (dict): Values to override during duplication.

        Returns:
            recordset: The new duplicated category record.
        """
        new_records = super(BookCategory, self).copy(default)
        for new_record in new_records:
            new_record.category_name = f"{new_record.category_name} (COPY)"
        return new_records

    def action_open_product_view(self):
        """
        Returns an action to open the related product.category form view.
        """
        book_category = self.env['product.category'].search([
            ('book_categ_id','=',self.id)
        ])
        if book_category:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.category',
                'res_id': book_category.id,
                'view_mode': 'form',
                'context': {'active_id': self.id},
                'target': 'current',        
            }
        return False