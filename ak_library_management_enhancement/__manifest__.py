# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'library management enhancement',
    'version': '19.0.1.2.1',
    'summary': """Manage Books""",
    'description': """We can Perform CRUD operations.""",
    'category': 'Library management',
    'author': 'Abhay sakariya',
    'company': 'Aktiv software',
    'website': 'https://www.aktivsoftware.com/',
    'depends': ['ak_library_management', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/library_book_views.xml',
        'views/book_category_views.xml',
        'views/book_edition_views.xml',
        'views/author_author_views.xml',
        'wizard/wizard_book_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
