# -*- coding: utf-8 -*-

{
    'name': 'library management search domain',
    'version': '19.0.1.1.1',
    'summary': """Manage Books""",
    'description': """i can perform domain operations.""",
    'category': 'Library management',
    'author': 'Abhay sakariya',
    'company': 'Aktiv software',
    'website': 'https://www.aktivsoftware.com/',
    'depends': ['ak_library_management_orm'],
    'data': [
        'security/ir.model.access.csv',
        'views/active_author_views.xml',
        'views/library_book_views.xml',
        'views/sale_order_view.xml',
        'wizard/book_wizard_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
