# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError


class BookOrderWizard(models.TransientModel):
    _name = 'book.order.wizard'
    _description = "Book Order"

    book_order_line_ids = fields.One2many(
        comodel_name='book.order.line.wizard',
        inverse_name='book_order_id',
        string="Order Lines",
    )
    is_editable = fields.Boolean()
    

    def default_get(self, vals):
        """
        Overrides the standard default_get method It sets default values when
        'edit_line' is true, populating 'book_order_line_ids' with the current 
        sale order's bookable products.

        Args:
            vals: A list of strings, where each string is the field name.

        Returns:
            dict : where the keys are the field names and the values are their
            corresponding default values.
        """
        res = super().default_get(vals)
        if self.env.context.get('edit_line'):
            res['is_editable'] = True
            sale_order = self.env['sale.order'].browse(
                self.env.context.get('active_id')
            )
            book_lines=[]
            for line in sale_order.order_line:
                if line.product_id.is_book_product:
                    book_lines.append(fields.Command.create({
                        'product_id':line.product_id.id,
                        'quantity':line.product_uom_qty
                    }))
            res['book_order_line_ids'] = book_lines
        return res
    
    def action_add_product(self):
        """
        Adds products from the wizard (`book_order_line_ids`) to the current
        Sale Order.If the product already exists in the sale order,
        it updates the quantity; otherwise, it creates a new line.

        Raise: class 'ValidationError' when lines not add or any line are not 
            add product or quantity is less then 1.
        
        Returns:
            Action to close the wizard window.
        """
        sale_order = self.env['sale.order'].browse(
            self.env.context.get('active_id')
        )
        if not self.book_order_line_ids:
            raise ValidationError("Please add at least one product.")
        for line in self.book_order_line_ids:
            if not line.product_id:
                raise ValidationError("Product required")
            if line.quantity <= 0:
                raise ValidationError("Quantity must be greate then 0")  
            existing_record = sale_order.order_line.filtered(
                lambda order_line:order_line.product_id == line.product_id
            )
            if existing_record:
                existing_record.product_uom_qty = line.quantity \
                if self.is_editable \
                else (existing_record.product_uom_qty + line.quantity)
            else:
                sale_order.order_line.create({
                    'order_id': sale_order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.product_id.lst_price
                })    
        sale_order.is_book_add = True
        return {'type': 'ir.actions.act_window_close'}
