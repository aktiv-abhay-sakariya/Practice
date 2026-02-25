# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, Command


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = "Books"

    name = fields.Char(string="Book Title", required=True)
    isbn = fields.Char(string='ISBN Number', required=True)
    publication_date = fields.Date(string='Date of Publication', required=True)
    price = fields.Float(string='Book Price', required=True)
    pages = fields.Integer(string='Number of Pages')
    description = fields.Html(string='Book Summary')
    image_1920 = fields.Image(string='Book Image')
    category_id = fields.Many2one(
        comodel_name='book.category',
        string='Category'
    )
    edition_ids = fields.Many2many(
        comodel_name='book.edition',
        string='Edition'
    )
    total_books = fields.Integer(
        string='Total Books',
        compute="_compute_total_book_and_sales"
    )
    total_sales_amout = fields.Float(
        string='Total sales amount',
        compute="_compute_total_book_and_sales"
    )
    author_id = fields.Many2one(
        comodel_name='author.author',
        string='Book Author'
    )
    author_scan = fields.Boolean(
        string='Computed Details',
        compute='_compute_book_details',
        store=True
    )

    @api.depends("edition_ids")
    def _compute_total_book_and_sales(self):
        """
        Calculates the total books and sales amount base on edition_ids.

        - total books : sum of quantity of each edition_ids.
        - total sales amount : sum of (quantity * book_price) of each
                               edition_ids.
        """
        book, total_sale = 0, 0
        for record in self:
            for one_book in record.edition_ids:
                book += one_book.quantity
                total_sale += (one_book.quantity * one_book.book_price)
        self.total_books = book
        self.total_sales_amout = total_sale

    @api.depends("author_id", "isbn", "publication_date", "price")
    def _compute_book_details(self):
        """
        Create or update or remove a record is automatically in
        author.book model.
        """
        for record in self:
            author_book = record.env['author.book'].search(
                [('book_id', '=', record.id)])
            if record.author_id:
                values = {
                    'isbn': record.isbn,
                    'publication_date': record.publication_date,
                    'price': record.price,
                    'book_id': record.id,
                    'author_id': record.author_id,
                }
                if author_book:
                    record.author_id.book_ids = [Command.update(
                        author_book.id, values
                    )]
                else:
                    record.author_id.book_ids = [Command.create(values)]
            else:
                author_book.unlink()
