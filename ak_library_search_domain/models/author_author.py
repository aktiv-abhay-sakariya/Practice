# -*- coding: utf-8 -*-

from odoo import api, models


class Author(models.Model):
    _inherit = 'author.author'
    

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        """
        Overrides name_search to filter active authors and search by name and
        author_ref
        """
        domain = domain or []
        domain += [('author_status','=','active')]
        if name:
            domain += [
                '|',
               ('name', operator, name),
               ('author_ref', operator, name)
            ]
        records = self.search_fetch(
            domain=domain,
            field_names=['id', 'name', 'author_ref']
        )
        result = [(record.id, record.display_name) for record in records]
        return result
 