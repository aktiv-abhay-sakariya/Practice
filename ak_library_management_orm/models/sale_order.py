# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state =  fields.Selection(
        [
            ('new', 'New'),
            ('approval_need', 'Approval'),
            ('done', 'Done')
        ],
        default='new',
        copy=False
    )
    is_manager_user = fields.Boolean(related="user_id.is_manager")
 
    def action_confirm(self):
        """
        Overrides the odoo standard action_confirm method Raise error if any
        book product in line has stock less than 5 And current user is not
        manager only allow manager to create and cancel SO.
        """
        if self.approval_state == 'new':
            low_stock_ids = self.order_line.filtered(
                lambda line:line.product_id.is_book_product and 
                line.product_id.qty_available < 5
            )
            if low_stock_ids:
                if not self.is_manager_user:
                    raise ValidationError(
                        "Approval needed! The following have low stock: %s"
                        % ', '.join(
                            [id.product_id.display_name for id in low_stock_ids]
                        )
                    )
                else:
                    self.approval_state = 'approval_need'
            else:
                self.approval_state = 'done'
        if self.approval_state == 'done':
            return super().action_confirm()
       
    def action_approve(self):
        """
        manager click the approve then change the approval_state.
        """
        self.approval_state = 'done'
    
    def action_reject(self):
        """
        manager click the rejcet then cancel sale order.
        """
        return self.action_cancel()
