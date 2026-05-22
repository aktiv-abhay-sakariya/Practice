# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software
# See LICENSE file for full copyright & licensing details.

from odoo import api, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        products.generate_internal_codes()
        return products

    def generate_internal_codes(self):
        for product in self:
            product.default_code = self.env['ir.sequence'].sudo().next_by_code('product.internal.reference')
            product.barcode = self.env['ir.sequence'].sudo().next_by_code('product.barcode')
