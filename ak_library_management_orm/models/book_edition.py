# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BookEdition(models.Model):
    _inherit = 'book.edition'
    
    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to ensure price and quantity
        are greater than zero.

        Args:
            vals (list): A list of dictionaries containing field values.

        Returns:
            recordset: The newly created book edition records.
        """
        for val in vals:
            if val.get('book_price', 0) <= 0:
                raise ValidationError("Price must be greater than zero.")
            if val.get('quantity', 0) <= 0:
                raise ValidationError("Quantity must be greater than zero.")
        return super(BookEdition, self).create(vals)

    def write(self, vals):
        """
        Overrides the standard write method to ensure updated price and 
        quantity are greater than zero.

        Args:
            vals (dict): A dictionary of fields and values being updated.

        Returns:
            bool: True if the record was updated successfully.
        """
        if 'book_price' in vals and vals['book_price'] <= 0:
            raise ValidationError("Price must be greater than zero.")
        if 'quantity' in vals and vals['quantity'] <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return super(BookEdition, self).write(vals)

    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)' to the 
        edition name.

        Args:
            default (dict): Values to override during duplication.

        Returns:
            recordset: The new duplicated edition record.
        """
        new_records = super(BookEdition, self).copy(default)
        for new_record in new_records:
            new_record.name = f"{new_record.name} (COPY)"
        return new_records
