# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approve_need = fields.Boolean(default=False)
    
    def action_confirm(self):
        print(self.approve_need)
        low_products = [line.product_id.name for line in self.order_line if line.product_id.qty_available < 5]
        if low_products and not self.approve_need:
            self.write({'approve_need':True})
            print(self.approve_need)
            raise UserError(f"Approval needed!\nThe following books have low stock:{low_products}")
        return self.action_confirm()

    def action_approve(self):
        if not self.env.user.is_manager:
            raise ValidationError(f"only manager can approve the order")
        return super().action_confirm()

    def action_reject(self):
        if not self.env.user.is_manager:
            raise ValidationError(f"only manager can reject the order")
        return self.action_cancel()
