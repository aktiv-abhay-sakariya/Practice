# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approve_need = fields.Boolean()
    is_manager_user = fields.Boolean(related="user_id.is_manager")
    
    def action_confirm(self):
        """
        Overrides the action_confirm method for check their order_line if any
        product have less then quantity then Validation error show.
        """
        if 'default_approve_need' in self.env.context:
            self.approve_need = self.env.context.get('default_approve_need')
        low_products = [
            line.product_id.display_name for line in self.order_line if
            line.product_id.qty_available < 5
        ]
        print(self.env.context)
        print(self.approve_need)
        if low_products and self.approve_need:
            raise ValidationError('low quantity')
        return super().action_confirm()

    def action_approve(self):
        """
        If usre are manager then order are confirm else give validation error.
        """
        if 'default_approve_need' in self.env.context:
            self.approve_need = self.env.context.get('default_approve_need')
        print(self.approve_need)
        if not self.is_manager_user:
            raise ValidationError(f"only manager can approve the order")

    def action_reject(self):
        """
        If usre are manager then order are cancel else give validation error.
        """
        if not self.is_manager_user:
            raise ValidationError(f"only manager can reject the order")
        return self.action_cancel()
