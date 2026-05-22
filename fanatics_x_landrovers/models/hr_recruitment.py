
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrJob(models.Model):
    _inherit = 'hr.job'

    minimum_education = fields.Char("Minimum Education")
    minimum_prior_experience = fields.Char("Minimum Prior Experience")
    required_prior_training = fields.Char("Required Prior Training")
    required_certifications = fields.Char("Required Certifications")
