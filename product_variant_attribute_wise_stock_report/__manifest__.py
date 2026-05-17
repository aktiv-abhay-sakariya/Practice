# -*- coding: utf-8 -*-

{
    "name": "Product Variant Attribute-wise Stock Report",
    "version": "19.0.1.0.0",
    "summary": "To display stock quantities of product variants by organizing them according to their attribute combinations",
    "description": """
        In Odoo, internal references (default_code) for product variants are not
        automatically generated based on the product template, which leads to
        manual effort and inconsistency.
        So this module use that automatically assigns and updates unique
        internal references for product variants at the time of variant creation.
    """,
    "category": "Sales/Sales",
    "author": "Aktiv software",
    "website": "https://www.aktivsoftware.com/",
    "depends": ["stock"],
    "data": [
        "views/product_report_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            'product_variant_attribute_wise_stock_report/static/src/js/product_selector.js',
            'product_variant_attribute_wise_stock_report/static/src/xml/product_selector.xml',
        ],
    },
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
}
