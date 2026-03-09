# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    book_categ_id = fields.Many2one(
        comodel_name='book.category',
        string = 'book product',
    )

    @api.model_create_multi
    def create(self, vals):
        # print(vals)
        # vals['name'] = vals['book_categ_id']
        record = super().create(vals)
        print(record)
        # parent_id = self.env['product.category'].search('name','=',vals.get('parent_categ_id'))
        return record