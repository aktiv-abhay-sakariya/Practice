# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Author(models.Model):
    _inherit = 'author.author'
    
    author_ref = fields.Char(
        string="Reference",
        copy=False,
        default="New",
        # groups='ak_library_management_orm.manager_access_group'
    )
    
    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to genrate and set author sequence.

        Args:
            vals (list): A dictionary of fields and values of this model.

        Returns:
            recordset : The newly created author records.
        """
        for val in vals:
            if val.get('author_ref', _("New")) == _("New"):
                val['author_ref'] = self.env['ir.sequence'].next_by_code(
                    'author.author'
                ) or _("New")
        return super().create(vals)

    def unlink(self):
        """
        Overrides the standard unlink method to remove related records in 
        'author.book' before deleting the author.

        Returns:
            bool: True if the deletion was successful.
        """
        for record in self:
            record.env['author.book'].search([
                ('author_id','=',record.id)
            ]).unlink()
        return super(Author, self).unlink()
    
    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)' to the author 
        name during record duplication.

        Args:
            default (dict): Dictionary of values to override during copy.

        Returns:
            recordset: The new duplicated record.
        """
        new_records = super(Author, self).copy(default)
        for new_record in new_records:
            new_record.name = f"{new_record.name} (COPY)"
        return new_records
