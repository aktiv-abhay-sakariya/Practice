from odoo import models, fields

class TrustConfirmWizard(models.TransientModel):
    _name = 'trust.confirm.wizard'
    _description = 'Trust Confirmation'

    sale_order_id = fields.Many2one('sale.order')

    def action_confirm_anyway(self):
        # This is called when the user clicks 'Continue' in the popup
        return self.sale_order_id.with_context(skip_trust_check=True).action_confirm()
