# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleBookWizard(models.TransientModel):
    _name = 'sale.book.wizard'
    _description = 'Add/Edit Books Wizard'

    sale_id = fields.Many2one('sale.order')

    line_ids = fields.One2many(
        'sale.book.wizard.line',
        'wizard_id',
        string="Books"
    )

    # -----------------------------
    # DEFAULT LOAD (EDIT MODE)
    # -----------------------------
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        if self.env.context.get('edit_mode'):
            sale = self.env['sale.order'].browse(
                self.env.context.get('default_sale_id')
            )

            lines = []
            for line in sale.order_line:
                if line.product_id.product_tmpl_id.is_book_product:
                    lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty
                    }))

            res['line_ids'] = lines

        return res

    # -----------------------------
    # VALIDATION + MERGE LOGIC
    # -----------------------------
    def action_add_books(self):
        self.ensure_one()

        if not self.line_ids:
            raise ValidationError("Please add at least one line.")

        sale = self.sale_id

        for line in self.line_ids:

            if not line.product_id:
                raise ValidationError("Product required.")

            if line.quantity <= 0:
                raise ValidationError("Quantity must be > 0.")

            existing_line = sale.order_line.filtered(
                lambda l: l.product_id == line.product_id
            )

            # -----------------------------
            # MERGE LOGIC
            # -----------------------------
            if existing_line:
                existing_line.product_uom_qty += line.quantity
            else:
                sale.order_line.create({
                    'order_id': sale.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.product_id.lst_price
                })

        # mark as added
        sale.is_book_added = True

        return {'type': 'ir.actions.act_window_close'}

    # -----------------------------
    # CANCEL
    # -----------------------------
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
   
   
 
class SaleBookWizardLine(models.TransientModel):
    _name = 'sale.book.wizard.line'

    wizard_id = fields.Many2one('sale.book.wizard')

    product_id = fields.Many2one(
        'product.product',
        domain="[('product_tmpl_id.is_book_product','=',True)]",
        required=True
    )

    quantity = fields.Float(default=1)