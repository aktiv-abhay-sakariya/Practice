
from odoo import models, fields, api, _
from odoo.exceptions import UserError

# Name	Type	Developer Comments	Context	Testing
# Critical Supplier	Boolean	Required field. Editable only by Purchasing Manager, or full Admin	ISO 9001-Purchasing Process	New request
# Outsourced Process	Boolean	Required field. Editable only by Purchasing Manager, or full Admin	ISO 9001-Outsourced Processes	New request
# Approval Status	Drop down list	Hardcode these values: Approved, Under Evaluation, Restricted, Disapproved	ISO 9001-Purchasing Process	New request

class ResPartner(models.Model):
    _inherit = 'res.partner'

    critical_supplier = fields.Boolean(string='Critical Supplier', required=False)
    outsourced_process = fields.Boolean(string='Outsourced Process', required=False)
    approval_status = fields.Selection([
        ('approved', 'Approved'),
        ('under_evaluation', 'Under Evaluation'),
        ('restricted', 'Restricted'),
        ('disapproved', 'Disapproved'),
    ], string='Approval Status')
    customer_id = fields.Integer(string='Customer ID', required=False)

    is_customer_contact = fields.Boolean(string='Is Customer Contact', required=False)
    nickname = fields.Char(string='Nickname', required=False)
    surname = fields.Char(string='Surname', required=False)

    display_name = fields.Char("Loan name", compute='_compute_display_name', store=False)

    @api.onchange('surname')
    def _onchange_surname(self):
        for rec in self:
            if not rec.nickname and rec.surname:
                rec.nickname = rec.surname

    def get_projects_of_customer(self, customer_id):
        project_ids = self.env['project.project'].sudo().search([('customer_id', '=', customer_id._origin.id)])
        return project_ids

    @api.onchange('nickname')
    def _onchange_nickname(self):
        for rec in self:
            if not rec.nickname:
                continue
            project_ids = self.get_projects_of_customer(rec)
            if project_ids:
                for project_id in project_ids:
                    project_id.nickname = rec.nickname

    @api.depends('name', 'nickname', 'is_customer_contact')
    def _compute_display_name(self):
        for partner in self:
            if partner.is_customer_contact:
                if self.env.user.has_group('fanatics_x_landrovers.group_can_see_restricted_partner_names'):
                    partner.display_name = partner.name
                else:
                    partner.display_name = partner.nickname if partner.nickname else "Customer #%s" % str(partner.id)
            else:
                partner.display_name = partner.name

    def read(self, fields=None, load='_classic_read'):
        """ Override read method to hide customer name
        """
        result = super().read(fields=fields, load=load)
        if fields and 'name' in fields:
            for partner in result:
                if partner.get('is_customer_contact') and partner['is_customer_contact']:
                    if not self.env.user.has_group('fanatics_x_landrovers.group_can_see_restricted_partner_names'):
                        partner['name'] = partner['nickname'] if partner['nickname'] else "Customer #%s" % str(partner['id'])
                        partner['street'] = ''  # Clear street to avoid showing address
                        partner['street2'] = ''  # Clear street2 to avoid showing address
                        partner['phone'] = ''
                        partner['mobile'] = ''
                        partner['zip'] = ''
                        partner['email'] = ''
        return result
