# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class VehicleDetail(models.Model):
    _name = 'vehicle.detail'
    _description = "Vehicle Details"
    _rec_name = "vehicle_name"

    vehicle_name = fields.Char(string = "Vehicle name", required = True)
    description = fields.Char(string = "Description")
    warranty_length = fields.Integer(string='Number of Year')
    total_projects = fields.Integer(compute="_compute_total_counts")
    total_donor_vehicles = fields.Integer(compute="_compute_total_counts")
    total_customer_requirements = fields.Integer(compute="_compute_total_counts")
    total_quality_alert = fields.Integer(compute="_compute_total_counts")
    total_service_warranty = fields.Integer(compute="_compute_total_counts")

    @api.constrains('vehicle_name')
    def _check_same_name(self):
        """
        Ensure that not create or copy record if name are allread exist in DB.

        :raise: class:'ValidationError' if any record create twice.
        """
        for rec in self:
            if rec.vehicle_name:
                records = rec.search_count(domain = [('vehicle_name', '=', rec.vehicle_name)])
                if records > 1:
                    raise ValidationError(
                        _("This vehicle name already stored.")
                    )

    def _compute_total_counts(self):
        for rec in self:
            rec.total_projects = self.env['project.project'].search_count([('vehicle_detail_id', '=', rec.id), ('project_is_vehicle_build', '=', True)])
            rec.total_donor_vehicles = self.env['donor.vehicle'].search_count([('vehicle_detail_id', '=', rec.id)])
            rec.total_customer_requirements = self.env['customer.requirements'].search_count([('vehicle_detail_id', '=', rec.id)])
            rec.total_quality_alert = self.env['quality.alert'].search_count([('vehicle_detail_ids', 'in', [rec.id])])
            rec.total_service_warranty = self.env['project.project'].search_count([('vehicle_detail_id', '=', rec.id), ('project_is_vehicle_build', '=', False)])

    def action_open_view(self):
        if self.env.context.get('is_project', False):
            name, model = 'Project', 'project.project'
            domain = [('vehicle_detail_id', '=', self.id), ('project_is_vehicle_build', '=', True)]
            records = self.env[model].search(domain)
        elif self.env.context.get('is_project_service_warranty', False):
            name, model = 'Project', 'project.project'
            domain = [('vehicle_detail_id', '=', self.id), ('project_is_vehicle_build', '=', False)]
            records = self.env[model].search(domain)
        elif self.env.context.get('is_donor_vehicle', False):
            name, model = 'Vehicle', 'donor.vehicle'
            domain = [('vehicle_detail_id', '=', self.id)]
            records = self.env[model].search(domain)
        elif self.env.context.get('is_customer_requirements', False):
            name, model = 'Customer', 'customer.requirements'
            domain = [('vehicle_detail_id', '=', self.id)]
            records = self.env[model].search(domain)
        elif self.env.context.get('is_quality_alert', False):
            name, model = 'Quality Alert', 'quality.alert'
            domain = [('vehicle_detail_ids', 'in', [self.id])]
            records = self.env[model].search(domain)
            print('\n\n',records)
        if len(records) == 1:
            return {
                'name': _('Project'),
                'type': 'ir.actions.act_window',
                'res_model': model,
                'res_id': records.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return {
            'name': _('Project'),
            'type': 'ir.actions.act_window',
            'res_model': model,
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
