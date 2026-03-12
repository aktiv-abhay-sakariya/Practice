# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _inherit = 'library.book'
    
    is_product_created = fields.Boolean(string='Show My Button',default=False)
    isbn = fields.Char(copy=False, default='New')

    def default_get(self, vals):
        """
        Overrides default_get to set default price and page count for new
        records.

        Args:
            vals (list): List of field names requesting a default value.

        Returns:
            dict: A dictionary mapping field names to their default values.
        """
        res = super().default_get(vals)
        res['price'] = 500
        res['pages'] = 100
        return res

    @api.model_create_multi
    def create(self, vals):
        """
        Overrides create to generate sequences and validate required fields 
        (category, editions, price, pages) for batch creation.

        Args:
            vals (list): A list of dictionaries containing field values.

        Returns:
            recordset: The newly created library.book records.
        """
        for val in vals:
            if val.get('isbn', _("New")) == _("New"):
                val['isbn'] = self.env['ir.sequence'].next_by_code(
                    'library.book'
                ) or _('New')
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
        Overrides write to enforce business rules on price, pages, and categories 
        during record updates.

        Args:
            vals (dict): Dictionary of fields and new values to update.

        Returns:
            bool: True if the update was successful.
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
        Overrides the standard copy method to append '(COPY)' to the book name.

        Args:
            default (dict): Values to override during duplication.

        Returns:
            recordset: The newly created duplicated book record.
        """
        new_records = super(LibraryBook, self).copy(default)
        for new_record in new_records:
            new_record.name = f"{new_record.name} (COPY)"
        return new_records

    def unlink(self):
        """
        Overrides unlink to clean up relations in 'author.book' before deletion.

        Returns:
            bool: True if the deletion was successful.
        """
        for record in self:
            record.env['author.book'].search([
                ('book_id', '=', record.id)
            ]).unlink()
        return super(LibraryBook, self).unlink()

    def create_product(self):
        """
        Create product of current book also create related category and
        attribute value.
        """
        for record in self:
            category = record._create_product_category(record.category_id)
            attribute_id = self.env['product.attribute'].search([
                ('name','=','Editions')
            ]).id
            attribute = record._create_product_attribute(
                attribute_id, record.edition_ids
            )
            product = self.env['product.template'].create({
                'name':record.name,
                'type':'consu',
                'is_storable':True,
                'categ_id':category.id,
                'book_id':record.id,
                'is_book_product':True,
                'attribute_line_ids':[Command.create({
                    'attribute_id':attribute_id,
                    'value_ids':[Command.set(attribute)]
                })]
            })
            record.is_product_created = True
            for variant in product.product_variant_ids:
                book_edition = self.env['book.edition'].search([(
                    'name',
                    '=',
                    variant.product_template_attribute_value_ids.name
                )],limit=1)
                if book_edition:
                    variant.write({
                        'lst_price': book_edition.book_price,
                        'qty_available':book_edition.quantity
                    })

    def _create_product_category(self, current_category):
        """
        Create product category related to current book category.
        
        Args:
            current_category: The book.category object(recordset) that are
            create in product.category.

        Returns:
            obj: Newly created product.category record it same as current
            book category.
        """
        product_category = self.env['product.category'].search(
            [('book_categ_id','=',current_category.id)]
        )
        if product_category:
            return product_category
        if current_category.parent_categ_id:
            product_category = self._create_product_category(
                current_category.parent_categ_id
            )
        product_category = self.env['product.category'].create({
            'name':current_category.category_name,
            'parent_id':product_category.id if product_category else False,
            'book_categ_id':current_category.id
        })
        return product_category
    
    def _create_product_attribute(self, attribute_id, editions):
        """
        Create Edition attribute value related to current book editions.
        
        Args:
            attribute_id: Edition's attribute id.
            editions: current book's editions records.

        Returns:
            list : list of ids Newly created edition value in
            product.attribute.value model.
        """
        attribute_value_ids = []
        for edition in editions:
            attribute_value = self.env['product.attribute.value'].search(
                [('name', '=', edition.name)]
            )
            if not attribute_value:
                attribute_value = self.env['product.attribute.value'].create({
                    'attribute_id':attribute_id,
                    'name':edition.name
                })
            attribute_value_ids.append(attribute_value.id)
        return attribute_value_ids
    
    def action_product_view(self):
        """
        Returns an action to open the related product template.
        """
        book_product = self.env['product.template'].search([
            ('book_id','=',self.id)
        ])
        if len(book_product) == 1:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'res_id': book_product.id,
                'view_mode': 'form',
                'context': {'active_id': self.id},
                'target': 'current',
            }
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'active_id': self.id},
            'target': 'current',
        }
        
    def send_email(self):
        """
        Sends an approval email using a template and logs the message in the
        chatter.
        """
        template = self.env.ref(
            'ak_library_management_orm.email_template_book_approved'
        )
        template.send_mail(
            self.id,
            force_send=True,
            email_values={'email_to':self.env['author.author'].browse(1).email}
        )
        self.message_post(
            body=f"Mail sent succesfully",
            message_type='comment',
        )
