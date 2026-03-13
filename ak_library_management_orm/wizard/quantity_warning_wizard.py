# -*- coding: utf-8 -*-
# Part of Aktiv software.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Author(models.TransientModel):
    _name = "product.quantity.wizard"


    message = fields.Char()
    
    def action_done(self):
        return {'type': 'ir.actions.act_window_close'}
