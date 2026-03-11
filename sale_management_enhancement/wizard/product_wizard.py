from odoo import models, fields

class TrustConfirmWizard(models.TransientModel):
    _name = 'product.confirm.wizard'
    _description = 'product Confirmation'

    sale_order_id = fields.Many2one('sale.order')

    def action_product_confirm_anyway(self):
        return self.sale_order_id.with_context(skip_product_item=True).check_order_line()
