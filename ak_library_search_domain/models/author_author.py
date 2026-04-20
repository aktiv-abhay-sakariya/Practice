# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import _, api, fields, models


class Author(models.Model):
    _name = 'author.author'
    _inherit = ['author.author', 'mail.thread', 'mail.activity.mixin']
    
    user_id = fields.Many2one(
        comodel_name = 'res.users',
        string = 'User',
        required = True
    )

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        """
        Overrides name_search to filter active authors and search by name and
        author_ref
        
        Return :
            list of pairs ``(id, display_name)`` for all matching records.
        """
        domain = domain or []
        domain += [('author_status','=','active')]
        if name:
            domain += ['|',
               ('name', operator, name),
               ('author_ref', operator, name)
            ]
        records = self.search_fetch(
            domain=domain,
            field_names=['id', 'name', 'author_ref']
        )
        result = [(record.id, record.display_name) for record in records]
        return result

    def _cron_update_author_status(self):
        """
        In record author_status change to inactive if author_status is new and
        create date is more than 10 days older and add a log not of that record.
        
        Return :
            None
        """
        records = self.env['author.author'].search([
                ('author_status', '=', 'new'),
                ('create_date', '<', fields.Date.today() - timedelta(days=10))
            ])
        for rec in records:
            rec.author_status = 'inactive'
            rec.message_post(
                body = _("""
                        This author has been automatically deactivated 
                        because the account was not activated within 10 days
                        of creation.
                    """),
                message_type = 'comment'
            )
