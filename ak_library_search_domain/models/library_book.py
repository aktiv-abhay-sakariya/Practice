# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['library.book', 'mail.thread', 'mail.activity.mixin']
    
    total_products = fields.Integer(
        string = "Products",
        compute="_compute_product_count"
    )
    
    is_mail_send = fields.Boolean()
    
    @api.constrains('name', 'author_id')
    def _check_same_book_and_author(self):
        """
        Ensure that not create or copy record if name and author_id of 
        that record allread exist.
        
        Raise: class:'ValidationError' if any record create twice.
        """
        for rec in self:
            if rec.author_id:
                domain = [
                    ('name', '=', rec.name),
                    ('author_id', '=', rec.author_id.id)
                ]
                records = rec.search_count(domain = domain)
                if records > 1:
                    raise ValidationError(
                        _("This author already has a book with the same name.")
                    )

    @api.depends('is_product_created')
    def _compute_product_count(self):
        """
        Count the total product variants of the book.
        
        Return : None
        """
        self.total_products = self.env['product.product'].search_count([
            ('book_id','=',self.id)
        ])

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        """
        Overrides name_search to search by book it's name, isbn and price
        
        Return : 
            list of tuple: tuple contain the record's id and display_name.
        """
        domain = domain or []
        if name:
            domain += ['|','|',
                ('name', operator, name),
                ('isbn', operator, name),
                ('price', '=', float(name) if name.isdigit() else 0),
            ]
            records = self.search_fetch(
                domain=domain,
                field_names=['display_name'],
                limit=limit
            )
            return [(rec.id, rec.display_name) for rec in records]
        return super().name_search(name, domain, operator, limit)

    @api.model_create_multi
    def create(self, vals):
        """
        Overrides the standard create method to add custom log not and 
        if author select then set activity and show notification.

        Args:
            vals: A dictionary of fields and values of this model.

        Returns:
            id (object): recordset of created new record.
        """
        records = super().create(vals)
        utc_tz = fields.Datetime.now()
        for rec in records:
            rec.message_post(
                body = _(f"""
                    Book {rec.name} has been created by {rec.create_uid.name} at 
                    {fields.Datetime.context_timestamp(self, utc_tz)}.
                """),
                message_type = 'comment'
            )
            if rec.author_id:
                rec.env['bus.bus']._sendone(
                    rec.author_id.user_id.partner_id,
                    'simple_notification',
                    {
                        'type': 'success',
                        'message': _(f"""
                            Your book {rec.name} is released by 
                            {rec.author_id.name} at 
                            {fields.Datetime.context_timestamp(self, utc_tz)}.
                        """),
                    }
                )
                rec.activity_schedule(
                    act_type_xmlid = 'mail.mail_activity_data_todo',
                    summary = _(f"Review your release {rec.name}"),
                    user_id = rec.author_id.user_id.id,
                    note = _('Please review the book. It is ready for release'),
                    date_deadline = (
                        fields.Datetime.context_timestamp(self, utc_tz) + 
                        timedelta(days=2)
                    )
                )
        return records

    def action_send_mail(self):
        """
        Sent a mail to author for confirmation message for his/her book 
        released successfully and add log note for email sent successfully.
        
        Return : None

        """
        self.ensure_one()
        if self.author_id and self.author_id.email and self.env.user.email:
            template = self.env.ref(
                "ak_library_search_domain.email_template_library_book",
                raise_if_not_found=False
            )
            if not template:
                raise ValidationError(
                    _("Mail template not found")
                )
            template.send_mail(
                self.id,
                force_send=True,
                email_values={'email_to':self.author_id.email}
            )
            self.message_post(
                body=f"E-mail was sent succesfully to {self.author_id.name}",
                message_type='comment',
            )
            self.is_mail_send = True
        else:
            raise ValidationError(
                _("Author's or Current User's Email-id not set yet")
            )
