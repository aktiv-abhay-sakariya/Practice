# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BookEdition(models.Model):
    _inherit = 'book.edition'
    
    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to enforce to price and quantity
        must be greater than zero during record creates.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            id (object): recordset of created new record
        """
        for val in vals:
            if val.get('book_price', 0) <= 0:
                raise ValidationError("Price must be greater than zero.")
            if val.get('quantity', 0) <= 0:
                raise ValidationError("Quantity must be greater than zero.")
        self.env['product.attribute.value'].create({'attribute_id':9,'name':val.get('name')})
        return super(BookEdition, self).create(vals)

    def write(self, vals):
        """
        Overrides the standard write method to enforce to price and quantity
        must be greater than zero during record updates.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            bool: True if a record updated succesfully otherwise False.
        """
        if 'book_price' in vals and vals['book_price'] <= 0:
            raise ValidationError("Price must be greater than zero.")
        if 'quantity' in vals and vals['quantity'] <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return super(BookEdition, self).write(vals)

    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)' at last in
        editiion name field during record copy.

        Args:
            default : default None.

        Returns:
            id (object): recordset of created new record.
        """
        new_records = super(BookEdition, self).copy(default)
        for new_record in new_records:
            new_record.name = f"{new_record.name} (COPY)"
        return new_records
