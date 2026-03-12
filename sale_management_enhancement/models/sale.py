# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trust = fields.Boolean(string="Trust")


    def action_confirm(self):
        if not self.env.context.get('skip_trust_check') and not self.trust:
            return {
                'name': 'Confirmation Required',
                'type': 'ir.actions.act_window',
                'res_model': 'trust.confirm.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_sale_order_id': self.id},
            }
        return self.check_order_line()

    def check_order_line(self):
        if self.env.context.get('skip_product_item'):
            return super().action_confirm()
        if not self.order_line:
            return {
                'name': 'Product alert',
                'type': 'ir.actions.act_window',
                'res_model': 'product.confirm.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_sale_order_id': self.id},
            }
        return super().action_confirm()