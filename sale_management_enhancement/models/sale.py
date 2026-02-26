# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trust = fields.Boolean(string="Trust")


    def action_confirm(self):
        if self.env.context.get('skip_trust_check'):
            return super().action_confirm()

        if not self.trust:
            return {
                'name': 'Confirmation Required',
                'type': 'ir.actions.act_window',
                'res_model': 'trust.confirm.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_sale_order_id': self.id},
            }
        return super().action_confirm()

