# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _inherit = 'library.book'

    def default_get(self, vals):
        """
        Overrides the standard default_get method it set default book price
        and page when record are new.

        Args:
            vals: A list of strings, where each string is the field name.

        Returns:
            dict : where the keys are the field names and the values are their
            corresponding default values.
        """
        res = super().default_get(vals)
        res['price'] = 500
        res['pages'] = 100
        return res

    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to enforce to have at least
        one category_id and edition_ids and price and page must be greater
        than zero during record creates.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            id (object): recordset of created new record.
        """
        for val in vals:
            if not val.get('category_id'):
                raise ValidationError("Category is required.")
            if not val.get('edition_ids'):
                raise ValidationError("Edition is required.")
            if val.get('price', 0) <= 0:
                raise ValidationError("Price must be greater than zero.")
            if val.get('pages', 0) <= 0:
                raise ValidationError("Pages must be greater than zero.")
        return super(LibraryBook, self).create(vals)

    def write(self, vals):
        """
        Overrides the standard write method to enforce to have at least
        one category_id and edition_ids and price and page must be greater
        than zero during record updates.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            bool: True if a record updated succesfully otherwise False.
        """
        update_book = super(LibraryBook, self).write(vals)
        if not self.category_id:
            raise ValidationError('Category is required.')
        if not self.edition_ids:
            raise ValidationError('At least one edition must exist.')
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")
        if self.pages <= 0:
            raise ValidationError("Pages must be greater than zero.")         
        return update_book

    def copy(self, default=None):
        """
        Overrides the standard copy method to append '(COPY)'at last in book
        name field during record copy.

        Returns:
            id (object): recordset of created new record.
        """
        new_records = super(LibraryBook, self).copy(default)
        for new_record in new_records:
            new_record.name = f"{new_record.name} (COPY)"
        return new_records

    def unlink(self):
        """
        Overrides the standard unlink method to enforce to remove current book
        relation in 'author.book' model then remove current book record.

        Args:
            default : default None.

        Returns:
            bool: True if a record remove succesfully in DB otherwise False.
        """
        for record in self:
            record.env['author.book'].search([('book_id', '=', record.id)]).unlink()
        return super(LibraryBook, self).unlink()

    def create_product(self):
        print('this is button method top')
        if self.author_id:
            # self.env['product_attribute_value_product_template_attribute_line_rel'].create()

            vals = {'name':self.name, 'type':'consu' ,'is_storable':True, 'book_id':self.id}
            print(vals)
            product_tmpl_id = self.env['product.template'].create(vals)
            
            # print('okkk - ')
            # # book_id = self.env['author.book'].search([('author_id','=',self.author_id),('book_id','=',self.id)])
        else:
            print('author not select')
        print('this is button method last')

