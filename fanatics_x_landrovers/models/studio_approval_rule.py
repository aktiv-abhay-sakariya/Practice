
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError

class StudioApprovalRule(models.Model):
    _inherit = 'studio.approval.rule'

    def _create_request(self, res_id):
        self.ensure_one()
        ruleSudo = self.sudo()

        if ruleSudo.approval_group_id:
            ruleSudo.approver_ids = ruleSudo.approval_group_id.users
        return super(StudioApprovalRule, self)._create_request(res_id)
