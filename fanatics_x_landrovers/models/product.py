
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductLevel1(models.Model):
    _name = 'product.level1'
    _description = 'Product Level 1'

    name = fields.Char(string='Name', required=True)


class ProductLevel2(models.Model):
    _name = 'product.level2'
    _description = 'Product Level 2'

    name = fields.Char(string='Name', required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    platform_usage = fields.Selection([('EV', 'EV'), ('ICE', 'ICE'), ('EV_ICE', 'EV & ICE')], string='Platform Usage')
    level_1 = fields.Many2one('product.level1', string='Level 1')
    level_2 = fields.Many2one('product.level2', string='Level 2')
    manufacturer_id = fields.Many2one('res.partner', string='Manufacturer')


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    manufacturer_id = fields.Many2one('res.partner', string='Manufacturer')
    manufacturer_code = fields.Char(string='Manufacturer Code')

