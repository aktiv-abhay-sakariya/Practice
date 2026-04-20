# -*- coding: utf-8 -*-

from odoo import fields, models


class BookOrderLineWizard(models.TransientModel):
    _name = 'book.order.line.wizard'
    _description = "Book Order Line"

    book_order_id = fields.Many2one(comodel_name='book.order.wizard')
    product_id = fields.Many2one(comodel_name='product.product')
    quantity = fields.Integer(default=1)
