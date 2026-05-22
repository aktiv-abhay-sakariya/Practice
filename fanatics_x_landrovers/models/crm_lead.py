from odoo import models, fields, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    won_project_is_created = fields.Boolean(string='Visible Project Smart Button',
                                                  compute='_compute_won_project_is_created')

    def _compute_won_project_is_created(self):
        for rec in self:
            project_id = self.env['project.project'].search([('won_lead_id', '=', self.id)], limit=1)
            if project_id:
                rec.won_project_is_created = True
            else:
                rec.won_project_is_created = False

    def action_create_project_from_won_opportunity(self):
        self.ensure_one()
        # Validation 1: Only Won stage
        if not self.stage_id.is_won:
            raise UserError(_("You can only create a project when the opportunity is in Won stage."))
        # Validation 2: Prevent duplicate
        won_project_id = self.env['project.project'].search([('won_lead_id', '=', self.id)], limit=1)
        if won_project_id:
            raise UserError(_("A project is already created for this opportunity."))
        action = self.env["ir.actions.actions"]._for_xml_id("project.open_create_project")
        action["context"] = dict(
            self.env.context,
            default_partner_id=self.partner_id.id,
            default_won_lead_id=self.id
        )
        return action

    # def action_open_project_won_opportunity(self):
    #     self.ensure_one()
    #
    #     project = self.env['project.project'].search(
    #         [('won_lead_id', '=', self.id)],
    #         limit=1
    #     )
    #
    #     if not project:
    #         return False
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Project Dashboard',
    #         'res_model': 'project.project',
    #         'view_mode': 'kanban,form',
    #         'views': [
    #             (self.env.ref('project.project_update_view_kanban').id, 'kanban'),
    #             (False, 'form'),
    #         ],
    #         'res_id': project.id,
    #         'domain': [('id', '=', project.id)],
    #         'target': 'current',
    #     }

    def action_open_project_won_opportunity(self):
        self.ensure_one()
        project_id = self.env['project.project'].search(
            [('won_lead_id', '=', self.id)],
            limit=1
        )
        if not project_id:
            return False
        action = self.env["ir.actions.actions"]._for_xml_id('project.project_update_all_action')
        action['display_name'] = _("%(name)s Dashboard", name=project_id.name)
        action['context'] = dict(
            self.env.context,
            active_id=project_id.id,
            active_ids=project_id.ids,
        )
        return action