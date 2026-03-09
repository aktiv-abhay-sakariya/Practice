# -*- coding: utf-8 -*-

from odoo import models


class Author(models.Model):
    _inherit = 'author.author'

    def unlink(self):
        """
        Overrides the standard unlink method to enforce to remove current author
        relation in 'author.book' model then remove current author record.

        Returns:
            bool: True if a record remove succesfully in DB otherwise False.
        """
        for record in self:
            record.env['author.book'].search([('author_id','=',record.id)]).unlink()
        return super(Author, self).unlink()
    
    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)'at last in author
        name field during record copy.

        Args:
            default : default None.

        Returns:
            id (object): recordset of created new record.
        """
        new_records = super(Author, self).copy(default)
        for new_record in new_records:
            new_record.name = f"{new_record.name} (COPY)"
        return new_records
