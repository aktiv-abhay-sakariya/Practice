
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
from datetime import timedelta

class LandRoverDefenderModel(models.Model):
    _name = 'landrover.defender.model'
    _description = 'Land Rover Defender Model'

    name = fields.Char(string='Name', required=True)


class LandRoverWheelBase(models.Model):
    _name = 'landrover.wheel.base'
    _description = 'Land Rover Wheel Base'

    name = fields.Char(string='Name', required=True)


class LandRoverSteering(models.Model):
    _name = 'landrover.steering'
    _description = 'Land Rover Steering'

    name = fields.Char(string='Name', required=True)


class LandRoverCountryExport(models.Model):
    _name = 'landrover.country.export'
    _description = 'Land Rover Country Export'

    name = fields.Char(string='Name', required=True)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    name = fields.Char(string="Project Name", required=False, tracking=True, compute='_compute_project_name', store=True,
                       readonly=False)
    nickname = fields.Char(string='Nickname', required=False)
    defender_model_id = fields.Many2one('landrover.defender.model', string='Defender Model', copy=False)
    wheel_base_id = fields.Many2one('landrover.wheel.base', string='Wheel Base', copy=False)
    steering_id = fields.Many2one('landrover.steering', string='Steering', copy=False)
    country_export_id = fields.Many2one('landrover.country.export', string='Country Export', copy=False)
    product_id = fields.Many2one('product.product', string='Car', copy=False)

    customer_id = fields.Many2one('res.partner', 'Customer Name', copy=False)
    donor_vehicle_vin = fields.Char('Donor Vehicle VIN Number', copy=False)

    quality_alert_ids = fields.Many2many('quality.alert', 'quality_alert_project_rel', 'project_id', 'alert_id', string='Quality Alerts', copy=False)
    count_quality_alerts = fields.Integer(compute='_compute_count_quality_alerts', string='Quality Alerts Count')
    count_donor_vehicle = fields.Integer(compute='_compute_count_donor_vehicle', string='Quality Donor Vehicle')

    export_country_ids = fields.Many2many('res.country', string='Export Countries', help='Countries where the vehicle is exported to.', copy=False)
    project_is_vehicle_build = fields.Boolean(compute='_compute_project_is_vehicle_build', string='Project is Vehicle Build', store=True)

    @api.depends('tag_ids')
    def _compute_project_is_vehicle_build(self):
        for record in self:
            record.project_is_vehicle_build = any(
                tag.name == 'Vehicle Build' for tag in record.tag_ids
            )
    number_of_weeks = fields.Integer(string="Number of Weeks", default=1)

    @api.onchange('number_of_weeks', 'date_start')
    def _onchange_planning_fields(self):
        for rec in self:
            # Only block if user sets weeks to 0 or less
            if rec.number_of_weeks is not None and rec.number_of_weeks <= 0:
                rec.number_of_weeks = rec._origin.number_of_weeks or 1
                raise UserError("Number of Weeks must be greater than zero.")
            # Auto calculate end date
            if rec.date_start and rec.number_of_weeks:
                rec.date = rec.date_start + timedelta(days=rec.number_of_weeks * 7)

    # @api.depends('tag_ids', 'build_slot_number', 'customer_id.surname', 'vehicle_name')
    # def _compute_project_name(self):
    #     """
    #     Computes the project name based on a structured format:
    #     Build-[ENGINE_TYPE_TAG]-[BUILD_NUMBER]-[CUSTOMER_SURNAME]-[VEHICLE_NAME]
    #     """
    #     for project in self.with_context(lang='en_GB'):
    #     # for project in self:
    #         name_parts = []
    #         engine_type_tag = False
    #
    #         # Find the relevant engine tag (ICE or EV)
    #         for tag in project.tag_ids:
    #             if tag.name.upper() in ('ICE', 'EV'):
    #                 engine_type_tag = tag.name.upper()
    #                 break  # Stop after finding the first relevant tag
    #
    #         # Proceed only if we have the essential parts: an engine tag and a build number
    #         if engine_type_tag and project.build_slot_number:
    #             name_parts.append(f"Build-{engine_type_tag}-{project.build_slot_number}")
    #
    #             if project.customer_id and project.customer_id.surname:
    #                 name_parts.append(project.customer_id.surname)
    #             if project.vehicle_name:
    #                 name_parts.append(project.vehicle_name)
    #
    #         if name_parts:
    #             project.name = "-".join(name_parts)
    #         else:
    #             # Fallback to avoid blank names
    #             if not project.name:
    #                 project.with_context(lang=None).name = _("New Project")
    #         if project.account_id:
    #             project.account_id.with_context(lang=None).name = project.name
    #         if project.documents_folder_id:
    #             project.documents_folder_id.with_context(lang=None).name = project.name

    @api.depends('tag_ids', 'build_slot_number', 'customer_id.nickname', 'nickname', 'vehicle_name')
    def _compute_project_name(self):
        languages = self.env['res.lang'].search([('active', '=', True)]).mapped('code')

        for project in self:
            name_parts = []
            engine_type_tag = False

            for tag in project.tag_ids:
                if tag.with_context(lang='en_GB').name.upper() in ('ICE', 'EV'):
                    engine_type_tag = tag.with_context(lang='en_GB').name.upper()
                    break

            if engine_type_tag and project.build_slot_number:
                name_parts.append(f"Build-{engine_type_tag}-{project.build_slot_number}")

                if project.nickname:
                    name_parts.append(project.nickname)

                if project.vehicle_name:
                    name_parts.append(project.vehicle_name)

            if name_parts:
                new_name = "-".join(name_parts)
            else:
                new_name = project.name or _("New Project")

            for lang in languages:
                project.with_context(lang=lang).name = new_name

            if project.account_id:
                for lang in languages:
                    project.account_id.with_context(lang=lang).name = new_name

            if project.documents_folder_id:
                for lang in languages:
                    project.documents_folder_id.with_context(lang=lang).name = new_name

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        for rec in self:
            nickname = ''
            if rec.customer_id and rec.customer_id.nickname:
                nickname = rec.customer_id.nickname
            rec.nickname = nickname

    @api.onchange('nickname')
    def _onchange_nickname(self):
        for rec in self:
            if rec.nickname:
                if rec.customer_id and not rec.customer_id.nickname:
                    rec.customer_id.nickname = rec.nickname

    @api.depends('quality_alert_ids')
    def _compute_count_quality_alerts(self):
        for project in self:
            project.count_quality_alerts = len(project.quality_alert_ids)

    def _compute_count_donor_vehicle(self):
        for project in self:
            donor_vehicle_ids = self.env['donor.vehicle'].sudo().search([('project_id', '=', project.id)]).ids
            project.count_donor_vehicle = len(donor_vehicle_ids)

    def action_view_quality_alerts(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("quality_control.quality_alert_action_check")
        action['domain'] = [('id', 'in', self.quality_alert_ids.ids)]
        action['context'] = {'default_project_ids': [(6, 0, [self.id])]}
        return action

    def process_tags(self):
        self.ensure_one()
        for tag in self.tag_ids:
            if tag.name.lower() == 'vehicle build':
                customer_requirement_id = self.env['customer.requirements'].search([('build_project_id', '=', self.id)])
                if not customer_requirement_id:
                    customer_requirement = self.env['customer.requirements'].create({
                        'build_project_id': self.id,
                        'customer_id': self.customer_id.id,
                    })

    @api.model_create_multi
    def create(self, vals_list):
        seq = None
        # Generate sequence only once
        if not self.env.context.get('build_seq_generated'):
            seq = self.env['ir.sequence'].next_by_code('project.build.slot.unique.number')
        if vals_list and seq:
            vals_list[0]['build_slot_number'] = str(seq)
        # Pass context to prevent duplicate sequence calls downstream
        projects = super(ProjectProject, self.with_context(build_seq_generated=True)).create(vals_list)
        projects.write({
            'build_slot_number': vals_list[0].get('build_slot_number', False),
            'vehicle_name': vals_list[0].get('vehicle_name', False),
            'render': vals_list[0].get('render', False),
            'build_summary_id': vals_list[0].get('build_summary_id', False),
            'donor_vehicle_id': vals_list[0].get('donor_vehicle_id', False),
            'export_country_ids': vals_list[0].get('export_country_ids', False),
            'partner_id': vals_list[0].get('partner_id', False),
            'customer_id': vals_list[0].get('partner_id', False),
            'allow_billable': vals_list[0].get('allow_billable', False),
        })
        for project in projects:
            if project.tag_ids:
                project.process_tags()
                if project.project_is_vehicle_build:
                    project.vehicle_detail_id = self.env['vehicle.detail'].search([('vehicle_name', '=', project.name)])
                    if not project.vehicle_detail_id:
                        project.vehicle_detail_id = self.env['vehicle.detail'].create({
                            'vehicle_name': project.name
                        })

            project._compute_project_name()
        return projects

    def _has_vehicle_build_tag(self):
        self.ensure_one()
        return any(tag.name == 'Vehicle Build' for tag in self.tag_ids)

    def write(self, vals):
        if 'partner_id' in vals and 'customer_id' not in vals:
            vals['customer_id'] = vals['partner_id']
        elif 'customer_id' in vals and 'partner_id' not in vals:
            vals['partner_id'] = vals['customer_id']
        res = super(ProjectProject, self).write(vals)
        if vals.get('tag_ids'):
            for project in self:
                if project.tag_ids:
                    project.process_tags()
        if 'name' in vals and not self.env.context.get('skip_name_sync'):
            languages = self.env['res.lang'].search([('active', '=', True)]).mapped('code')
            new_name = vals['name']
            for project in self:
                for lang in languages:
                    project.with_context(lang=lang, skip_name_sync=True).name = new_name
                if project.account_id:
                    for lang in languages:
                        project.account_id.with_context(lang=lang).name = new_name
                if project.documents_folder_id:
                    for lang in languages:
                        project.documents_folder_id.with_context(lang=lang).name = new_name
        return res

    def action_open_donor_vehicle(self):
        self.ensure_one()
        action = self.env.ref('fanatics_x_landrovers.action_donor_vehicle').sudo().read()[0]
        donor_vehicle_ids = self.env['donor.vehicle'].sudo().search([
            ('project_id', '=', self.id)
        ])
        if donor_vehicle_ids:
            domain = [('id', 'in', donor_vehicle_ids.ids)]
        else:
            domain = [('id', '=', False)]
        action.update({
            'view_mode': 'list,form',
            'views': [
                (self.env.ref('fanatics_x_landrovers.view_donor_vehicle_list').id, 'list'),
                (self.env.ref('fanatics_x_landrovers.view_donor_vehicle_form').id, 'form'),
            ],
            'domain': domain,
        })
        return action

    def _get_stat_buttons(self):
        buttons = super()._get_stat_buttons()
        buttons.append({
            'icon': 'car',
            'text': self.env._('Donor Vehicles'),
            'number': self.count_donor_vehicle,
            'action_type': 'object',
            'action': 'action_open_donor_vehicle',
            'additional_context': json.dumps({
                'active_id': self.id,
            }),
            'show': True,
            'sequence': 99,
        })
        buttons.append({
            'icon': 'user',
            'text': self.env._('Customer'),
            'action_type': 'object',
            'action': 'action_open_won_opportunity_of_project',
            'additional_context': json.dumps({
                'active_id': self.id,
            }),
            'show': bool(self.won_lead_id),
            'sequence': 99,
        })
        return buttons

    def action_open_won_opportunity_of_project(self):
        self.ensure_one()
        if not self.won_lead_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer',
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'res_id': self.won_lead_id.id,
            'target': 'current',
        }

class ProjectTask(models.Model):
    _inherit = 'project.task'

    bom_ids = fields.Many2many('mrp.bom', string='Bill of Materials')
    product_ids = fields.Many2many('product.product', string='Products')

    def write(self, vals):
        if 'stage_id' in vals and self.env['project.task.type'].browse(vals['stage_id']).name == 'In Progress':
            if self.bom_ids:
                self.env['mrp.production'].create({
                    'bom_id': self.bom_ids[0].id,
                    'product_id': self.bom_ids[0].product_tmpl_id.product_variant_id.id,
                    'product_qty': 1,
                })
        return super(ProjectTask, self).write(vals)