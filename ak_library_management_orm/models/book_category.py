# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError


class BookCategory(models.Model):
    _inherit = 'book.category'

    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to enforce to prevent loop
        during record creates.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            id (object): recordset of created new record
        """
        self._prevent_loop(vals)
        record = super(BookCategory, self).create(vals)
        self.env['product.category'].create({'name':record.category_name,'book_categ_id':record.id})
        return record

    def write(self, vals):
        """
        Overrides the standard write method to enforce to prevent loop
        during record updates.

        Args:
            vals: A dictionary of fields and values being updated.

        Returns:
            bool: True if a record updated succesfully otherwise False.
        """
        print(vals)
        self._prevent_loop(vals)
        return super(BookCategory, self).write(vals)

    def _prevent_loop(self, vals):
        """
        Checks if a record creates a parent-child loop.

        Args:
            vals (dict): A dictionary of fields and values.
        """
        if 'parent_categ_id' in vals:
            if (self.id == vals['parent_categ_id'] or 
                self._check_category_loop(self.env['book.category'].search([
                    ('id','=',vals['parent_categ_id'])
                ]))):
                raise UserError('You cannot set a category as its own parent')

    def _check_category_loop(self, category):
        """
        Recursively checks if a given category ID is a parent category of
        the current category.

        Args:
            category : The category object(recordset) to check in the hierarchy.

        Returns:
            bool: True if a loop is detected otherwise False.
        """
        while category:
            if category.id == self.id:
                return True
            category = category.parent_categ_id
        return False

    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)'at last in
        category name field during record copy.

        Args:
            default : default None.

        Returns:
            id (object): recordset of created new record.
        """
        new_records = super(BookCategory, self).copy(default)
        for new_record in new_records:
            new_record.category_name = f"{new_record.category_name} (COPY)"
        return new_records
