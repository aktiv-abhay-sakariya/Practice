# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approve_need = fields.Boolean()
    
    def action_confirm(self):
        low_products = [line.product_id.name for line in self.order_line if line.product_id.qty_available < 5]
        if low_products and not self.approve_need:
            self.approve_need = True
            return {
                'name': _("Product quantity warning"),
                'type': 'ir.actions.act_window',
                'res_model': 'product.quantity.wizard',
                'target': 'new',
                'view_mode': 'form',
                'context': {
                    'active_id': self.id,
                    'default_message': low_products
                },
            }
        self.approve_need = False
        return super().action_confirm()

    def action_approve(self):
        if not self.env.user.is_manager:
            raise ValidationError(f"only manager can approve the order")
        return self.action_confirm()

    def action_reject(self):
        if not self.env.user.is_manager:
            raise ValidationError(f"only manager can reject the order")
        self.approve_need = False
        return self.action_cancel()
