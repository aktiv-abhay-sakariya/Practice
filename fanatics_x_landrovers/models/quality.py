
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class QualityAlert(models.Model):
    _inherit = 'quality.alert'

    project_ids = fields.Many2many('project.project', 'quality_alert_project_rel', 'alert_id', 'project_id', string='Related Projects', tracking=True)
    vehicle_detail_ids = fields.Many2many('vehicle.detail', string='New Vehicle Name', compute="_compute_vehicle_detail_ids", store=True)

    @api.depends('project_ids')
    def _compute_vehicle_detail_ids(self):
        for rec in self:
            if rec.project_ids:
                rec.vehicle_detail_ids = rec.project_ids.mapped('vehicle_detail_id')
            else:
                rec.vehicle_detail_ids = None