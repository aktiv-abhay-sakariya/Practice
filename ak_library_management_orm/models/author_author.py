# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Author(models.Model):
    _inherit = 'author.author'
    
    author_ref = fields.Char(
        string="Reference",
        copy=False,
        default="New",
        groups='ak_library_management_orm.manager_access_group'
    )
    
    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to genrate and set author sequence.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            id (object): recordset of created new record.
        """
        for val in vals:
            if val.get('author_ref', "New") == "New":
                val['author_ref'] = self.env['ir.sequence'].next_by_code(
                    'author.author'
                )
        return super().create(vals)

    def unlink(self):
        """
        Overrides the standard unlink method to enforce to remove current author
        relation in 'author.book' model then remove current author record.

        Returns:
            bool: True if a record remove succesfully in DB otherwise False.
        """
        for record in self:
            record.env['author.book'].search([
                ('author_id','=',record.id)
            ]).unlink()
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
