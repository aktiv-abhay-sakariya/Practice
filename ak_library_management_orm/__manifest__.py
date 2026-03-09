# -*- coding: utf-8 -*-

{
    'name': 'library management ORM',
    'version': '19.0.1.0.1',
    'summary': """Manage Books""",
    'description': """We can Perform ORM method operations.""",
    'category': 'Library management',
    'author': 'Abhay sakariya',
    'company': 'Aktiv software',
    'website': 'https://www.aktivsoftware.com/',
    'depends': [ 'sale_management', 'stock', 'ak_library_management'],
    'data': [
        'data/product_attribute_data.xml',
        'views/library_book_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
