# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'sale management enhancement',
    'version': '19.0.1.0.0',
    'summary': """Manage sale""",
    'description': """We can Perform CRUD operations.""",
    'category': 'sale',
    'author': 'Abhay sakariya',
    'company': 'Aktiv software',
    'website': 'https://www.aktivsoftware.com/',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_enhancement_view.xml',
        'wizard/trust_wizard_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
