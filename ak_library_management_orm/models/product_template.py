# -*- coding: utf-8 -*-


from odoo import api, fields, models, Command


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_book_product = fields.Boolean(string = 'book product', default = True)
    book_id = fields.Many2one(
        comodel_name='library.book',
        string = 'book product',
    )

    @api.model_create_multi
    def create(self, vals):
        record = super().create(vals)
        record.categ_id = self.env['product.category'].search([('name','=',record.book_id.category_id.category_name)]).id
        attribute_value_ids = []
        for edition in record.book_id.edition_ids:
            attribute_value = self.env['product.attribute.value'].search(
                [('name', '=', edition.name)], limit=1
            )
            if attribute_value:
                attribute_value_ids.append(attribute_value.id)
        print(attribute_value_ids)
        self.env['product.template.attribute.line'].create({
            'product_tmpl_id': record.id,
            'attribute_id': 9,
            'value_ids': [Command.set(attribute_value_ids)] 
        })
        print('this is product template file')
        return record