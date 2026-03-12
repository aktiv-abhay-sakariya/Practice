# -*- coding: utf-8 -*-

{
    'name': 'library management ORM',
    'version': '19.0.1.1.1',
    'summary': """Manage Books""",
    'description': """We can Perform ORM method operations.""",
    'category': 'Library management',
    'author': 'Abhay sakariya',
    'company': 'Aktiv software',
    'website': 'https://www.aktivsoftware.com/',
    'depends': [ 'sale_management', 'stock', 'ak_library_management_enhancement'],
    'data': [
        'security/custom_group.xml',
        'data/product_attribute_data.xml',
        'data/library_book_sequence.xml',
        'data/author_author_sequence.xml',
        'data/mail_template.xml',
        'views/library_book_views.xml',
        'views/author_author_views.xml',
        'views/book_category_views.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
