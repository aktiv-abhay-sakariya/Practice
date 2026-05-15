# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def select_product_template(self, product, category):
        print('\n\n',product)
        print('\n\n',category)
        return {}