
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.depends("name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.name


class BuildSummary(models.Model):
    _name = 'build.summary'
    _description = 'Build Summary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'project_id'

    build_slot_number_id = fields.Integer(related='project_id.build_slot_number', string='Build Slot Number')
    contact_name_id = fields.Many2one('res.partner', string='Contact Name')
    project_id = fields.Many2one('project.project', string='Project')
    project_image_id = fields.Image(string='Project Image')
    donor_vehicle_vin_id = fields.Char(string='Donor Vehicle-VIN')
    sales_orders_ids = fields.One2many('sale.order', 'build_summary_id', string='Sales Orders')
    manufacturing_orders_ids = fields.One2many('mrp.production', 'build_summary_id', string='Manufacturing Orders')
    invoices_ids = fields.One2many('account.move', 'build_summary_id', string='Invoices')
    customer_requirements_ids = fields.One2many('customer.requirements', 'build_summary_id', string='Customer Requirements')


class CustomerRequirements(models.Model):
    _name = 'customer.requirements'
    _description = 'Customer Requirements'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'vehicle_name'

    build_project_id = fields.Many2one('project.project', string='Build Project')
    build_slot_number_id = fields.Integer(related='build_project_id.build_slot_number', string='Build Slot Number')
    customer_id = fields.Many2one('res.partner', string='Customer', related='build_project_id.customer_id')
    vehicle_name = fields.Char(related='build_project_id.vehicle_name', string='Vehicle Name')
    vehicle_detail_id = fields.Many2one('vehicle.detail', string='New Vehicle Name', related="build_project_id.vehicle_detail_id")
    attribute_ids = fields.One2many('customer.requirements.attribute', 'customer_requirements_id', string='Attributes')
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    option_id = fields.Many2one('product.attribute.value', string='Option')
    # decision_stage_ids = fields.One2many('project.task', 'customer_requirements_id', string='Decision Stage')
    # decision_so_ids = fields.One2many('sale.order', 'customer_requirements_id', string='Decision SO')

    build_summary_id = fields.Many2one('build.summary', string='Build Summary')

    _rec_name = 'vehicle_name'


class CustomerRequirementsAttribute(models.Model):
    _name = 'customer.requirements.attribute'
    _description = 'Customer Requirements Attribute'

    customer_requirements_id = fields.Many2one('customer.requirements', string='Customer Requirements')
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    option_id = fields.Many2one('product.attribute.value', string='Option', domain="[('attribute_id', '=', attribute_id)]")
    decision_so_ids = fields.Many2many('sale.order', string='Decision SO')
    customer_decision_deadline = fields.Date(string='Customer Decision Deadline')

class DonorVehicle(models.Model):
    _name = 'donor.vehicle'
    _description = 'Donor Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'project_id'

    extra_chassis_number_a = fields.Char(string='a.', tracking=1)
    extra_chassis_number_a1 = fields.Char(string='a1.', tracking=1)
    extra_chassis_number_a2 = fields.Char(string='a2.', tracking=1)
    extra_chassis_number_b = fields.Char(string='b.', tracking=1)
    extra_chassis_number_c = fields.Char(string='c.', tracking=1)
    extra_chassis_number_d = fields.Char(string='d.', tracking=1)
    extra_chassis_number_e = fields.Char(string='e.', tracking=1)
    engine_number = fields.Char(string='Engine number', tracking=1)
    gearbox_number = fields.Char(string='Gearbox number', tracking=1)
    t_case_number = fields.Char(string='T-case number', tracking=1)
    axle_number_rear = fields.Char(string='Axle number rear', tracking=1)
    axle_number_front = fields.Char(string='Axle number front', tracking=1)
    vehicle_name = fields.Char(string='Vehicle Name', related='project_id.vehicle_name', tracking=1)
    vehicle_detail_id = fields.Many2one('vehicle.detail', string='New Vehicle Name', related="project_id.vehicle_detail_id")
    build_slot_number_id = fields.Integer(related='project_id.build_slot_number', string='Build Slot Number', tracking=1)
    customer_id = fields.Many2one('res.partner', related='project_id.partner_id', string='Customer', tracking=1)
    age = fields.Char(string='Age', compute='_compute_age', tracking=1)
    country_of_origin_id = fields.Many2one('res.country', string='Country of Origin', tracking=1)
    motor_id = fields.Many2one('product.attribute.value', string='Motor', domain="[('attribute_id', 'ilike', 'ICE Engine Type')]", tracking=1)
    build_date = fields.Date(string='Build Date', tracking=1)
    wheelbase = fields.Selection([
        ('90', '90'),
        ('110', '110'),
        ('130', '130')
    ], string='Wheelbase', tracking=1)
    license_plate = fields.Char(string='License Plate', tracking=1)
    location_id = fields.Many2one('stock.location', string='Location of Car', tracking=1)
    purchase_date = fields.Date(string='Purchase Date', tracking=1)
    purchase_price = fields.Monetary(string='Purchase Price', tracking=1)
    currency_id = fields.Many2one('res.currency', string='Currency', tracking=1)
    purchased_from_id = fields.Many2one('res.partner', string='Purchased From', tracking=1)
    purchased_by_which_entity = fields.Selection([
        ('BV', 'BV'),
        ('Z&O', 'Z&O')
    ], string='Purchased By Which Entity', tracking=1)
    doc = fields.Boolean(string='DoC', tracking=1)
    doc_images = fields.Binary(string='DoC Images')
    heritage_certificate = fields.Boolean(string='Heritage Certificate', tracking=1)

    heritage_certificate_image = fields.Binary(string='Heritage Certificate Image', tracking=1)
    heritage_certificate_file = fields.Image(string='Heritage Certificate file')
    vin_checked = fields.Boolean(string='VIN Checked', tracking=1)
    id_plate_present = fields.Boolean(string='ID Plate Present')
    id_plate_location_id = fields.Many2one('stock.location', string='ID Plate Location', tracking=1)
    id_plate_responsible_person_id = fields.Many2one('res.partner', string='ID Plate Responsible Person', tracking=1)
    folder_admin = fields.Char(string='Folder Admin', tracking=1)
    in_dor = fields.Boolean(string='In DOR', tracking=1)
    appraised = fields.Boolean(string='Appraised', tracking=1)
    rdw_imported_nl_license_plate = fields.Boolean(string='RDW - Imported / NL License Plate', tracking=1)
    rdw_labelled = fields.Boolean(string='RDW Labelled', tracking=1)
    rdw_label_ids = fields.One2many('donor.vehicle.label', 'donor_vehicle_id', string='RDW Labels')
    build_summary_id = fields.Many2one('build.summary', string='Build Summary', tracking=1)

    lot_id = fields.Many2one('stock.lot', string='Lot/Serial Number', tracking=1)
    location_id = fields.Many2one('stock.location', string='Location', tracking=1)


    own_chassis = fields.Boolean(string='Own Chassis', tracking=1)
    used_new_chassis = fields.Boolean(string='Used a new chassis (Marsland)', tracking=1)
    new_chassis_serial = fields.Char(string='New Chassis Serial (Marsland)', tracking=1)
    drive_side = fields.Selection([
        ('LHD', 'LHD'),
        ('RHD', 'RHD')
    ], string='Drive Side', tracking=1)
    internal_notes = fields.Html(string='Internal Notes')
    rdw_lost_label = fields.Boolean(string='RDW Lost Label', tracking=1)
    rdw_lost_labels = fields.Boolean(string='RDW Lost Labels?', compute='_compute_rdw_lost_labels', store=True, tracking=1)
    build_stage_id = fields.Many2one('project.task', string='Build Stage', tracking=1)
    donor_state = fields.Selection([
        ('Not Stripped', 'Not Stripped'),
        ('Stripped', 'Stripped')
    ], string='Donor State', tracking=1)

    project_id = fields.Many2one('project.project', string='Project', tracking=1)

    _rec_name = 'lot_id'

    def _compute_age(self):
        for record in self:
            # record.age needs to be 14y3m so %sy%sm
            if record.build_date:
                age = fields.Date.today() - record.build_date
                years = age.days // 365
                months = (age.days % 365) // 30
                record.age = f"{years}y{months}m"
            else:
                record.age = False

    @api.depends('rdw_label_ids', 'rdw_label_ids.rdw_lost_label')
    def _compute_rdw_lost_labels(self):
        for record in self:
            record.rdw_lost_labels = any(label.rdw_lost_label for label in record.rdw_label_ids)

    def write(self, vals):
        if self.env.context.get("skip_sync"):
            return super().write(vals)

        old_map = {rec.id: rec.project_id.id for rec in self}

        res = super().write(vals)

        if "project_id" in vals:
            Project = self.env["project.project"]

            for rec in self:
                new_project = rec.project_id
                old_project_id = old_map.get(rec.id)

                # unlink old project
                if old_project_id and (not new_project or old_project_id != new_project.id):
                    old_project = Project.browse(old_project_id)
                    if old_project.exists() and old_project.donor_vehicle_id.id == rec.id:
                        old_project.with_context(skip_sync=True).write({
                            "donor_vehicle_id": False
                        })

                # link new project
                if new_project:
                    if new_project.donor_vehicle_id and new_project.donor_vehicle_id.id != rec.id:
                        new_project.donor_vehicle_id.with_context(skip_sync=True).write({
                            "project_id": False
                        })

                    new_project.with_context(skip_sync=True).write({
                        "donor_vehicle_id": rec.id
                    })

        return res


class DonorVehicleLabel(models.Model):
    _name = 'donor.vehicle.label'
    _description = 'Donor Vehicle Label'

    donor_vehicle_id = fields.Many2one('donor.vehicle', string='Donor Vehicle')
    rdw_label_id = fields.Char(string='RDW Label ID')
    rdw_label_location_on_car = fields.Char(string='RDW Label Location on Car')
    rdw_label_photo = fields.Binary(string='RDW Label Photo')
    rdw_lost_label = fields.Boolean(string='RDW Lost Label')

class ProjectProject(models.Model):
    _inherit = 'project.project'

    build_slot_number = fields.Integer(string='Build Slot Number', copy=False)
    vehicle_name = fields.Char(string='Vehicle Name', copy=False)
    vehicle_detail_id = fields.Many2one('vehicle.detail', string='New Vehicle Name')
    render = fields.Binary(string='Render', copy=False)
    customer_requirements_ids = fields.One2many('customer.requirements', 'build_project_id', string='Customer Requirements', copy=False)
    #stage_sales_orders_ids = fields.One2many('sale.order', 'project_id', string='Stage Sales Orders')
    build_summary_id = fields.Many2one('build.summary', string='Build Summary', copy=False)

    donor_vehicle_id = fields.Many2one('donor.vehicle', string='Donor Vehicle VIN Number', copy=False)
    won_lead_id = fields.Many2one('crm.lead', string="Won Opportunity", copy=False)

    def write(self, vals):
        if self.env.context.get("skip_sync"):
            return super().write(vals)

        old_map = {rec.id: rec.donor_vehicle_id.id for rec in self}

        res = super().write(vals)

        if "donor_vehicle_id" in vals:
            Vehicle = self.env["donor.vehicle"]

            for rec in self:
                new_vehicle = rec.donor_vehicle_id
                old_vehicle_id = old_map.get(rec.id)

                # unlink old vehicle if changed/removed
                if old_vehicle_id and (not new_vehicle or old_vehicle_id != new_vehicle.id):
                    old_vehicle = Vehicle.browse(old_vehicle_id)
                    if old_vehicle.exists() and old_vehicle.project_id.id == rec.id:
                        old_vehicle.with_context(skip_sync=True).write({
                            "project_id": False
                        })

                # link new vehicle
                if new_vehicle:
                    # ensure one-to-one
                    if new_vehicle.project_id and new_vehicle.project_id.id != rec.id:
                        new_vehicle.project_id.with_context(skip_sync=True).write({
                            "donor_vehicle_id": False
                        })

                    new_vehicle.with_context(skip_sync=True).write({
                        "project_id": rec.id
                    })

        return res


class ProjectTask(models.Model):
    _inherit = 'project.task'

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    build_summary_id = fields.Many2one('build.summary', string='Build Summary')


class AccountMove(models.Model):
    _inherit = 'account.move'

    build_summary_id = fields.Many2one('build.summary', string='Build Summary')

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    build_summary_id = fields.Many2one('build.summary', string='Build Summary')
