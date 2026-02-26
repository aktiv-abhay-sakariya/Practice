# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.
from itertools import product

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trust = fields.Boolean(string="Trust")

    def action_confirm(self):
        if self.trust:
            products = self.env['sale.order.line'].search([('order_id', '=', self.id)])
            if products:
                total = 0
                for product in products:
                    total += product.price_total
                print("total price : ",total)
            else:
                print('no products')
        else:
            print('no trust')
        return super().action_confirm()