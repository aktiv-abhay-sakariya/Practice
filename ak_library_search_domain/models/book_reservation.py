# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class BookReservation(models.Model):
    _name = 'book.reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Book Reservation'
    _rec_name = 'book_id'
    
    customer_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Customer',
        required = True
    )
    book_id = fields.Many2one(
        comodel_name = 'library.book',
        string = 'Book',
        required = True
    )
    reservation_date = fields.Date(
        string='Reservation Date',
        default = fields.Date.today()
    )
    expected_pickup_date = fields.Date(
        string='Picked Up',
        required = True
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('reserved', 'Reserved'),
            ('cancel', 'Cancelled'),
            ('pickup', 'Picked Up')
        ],
        string = "status",
        default='draft',
    )

    def book_reservation_analysis(self):
        """
        Opens a book reservation graph view with filter state and group by
        book_id.
        
        Return : 
            dict:A dictionary representing the window action for the graph view.
        """
        return {
            'name': 'Reservation Analysis',
            'type': 'ir.actions.act_window',
            'res_model': 'book.reservation',
            'view_mode': 'graph',
            'target': 'current',
            'context': {'is_book_analysis_view': True}
        }

    @api.model
    def _read_group(self, domain, groupby=(), aggregates=(), having=(), offset=0, limit=None, order=None):
        """
        Overrides _read_group to apply special filtering and grouping for
        book analysis.

        Args: 
            domain: Initial search domain.
            groupby: List of fields to group by.
            aggregates: List of aggregation specification.
            having: Filter for aggregated data.
            offset: optional number of groups to skip.
            limit: optional max number of groups to return.
            order: Sorting criteria.
        
        Return : 
            list of tuples: it containing in the order the groups values and
            aggregates values.
        """
        if self.env.context.get('is_book_analysis_view'):
            domain = domain or [] + [('state', '=', 'reserved')]
            groupby = ['book_id']
        return super()._read_group(
            domain, groupby, aggregates, having, offset, limit, order
        )

    @api.model
    def search_fetch(self, domain, field_names=None, offset=0, limit=None, order=None):
        """
        Overrides search_fetch to apply special domain for customer views.
        
        Args:
            domain: Initial search domain.
            field_names: a collection of field names to fetch.
            offset: optional, 'mail.threa number of groups to skip.
            limit: optional max number of groups to return.
            order: Sorting criteria.

        Return :
            record-sets: records matching the search criteria.
        """
        if self.env.context.get('is_customer_view'):
            domain = domain or [] + [
                    ('customer_id', '=', self.env.context.get('active_id')),
                    ('state', '=', 'reserved')
                ]
        return super().search_fetch(domain, field_names, offset, limit, order)

    def action_cancel_overdue_reservation(self):
        """
        In record state change to cancel if state is reserved and the pick up 
        date is earlier than the current date and add a log not of that record.
        
        Return :
            None
        """
        for rec in self:
            if rec.state == 'reserved' and \
                rec.expected_pickup_date < fields.Date.today():
                rec.state = 'cancel'
                rec.message_post(
                    body = _("""
                        The reservation was cancelled because the pickup 
                        date has passed.
                    """),
                    message_type = 'comment'
                )

    def _cron_update_book_status(self):
        """
        In record state change to cancel if state is reserved and the pick up 
        date is earlier than the current date and add a log not of that record
        and log print in odoo server log.
        
        Return : 
            None
        """
        records = self.env['book.reservation'].search([
                ('state', '=', 'reserved'),
                ('expected_pickup_date', '<', fields.Date.today())
            ])
        for rec in records:
            rec.state = 'cancel'
            rec.message_post(
                body = _("The reservation was cancelled automatically."),
                message_type = 'comment'
            )
            _logger.info(
                f"""book : {rec.book_id.name} is cancelled due to 
                overdue reservations""",
            )

    def action_send_mail(self):
        """
        Open a mail composer for sent a mail to customer for confirmation
        message for his/her book reserved successfully.
        
        Return : None

        """
        self.ensure_one()
        if self.customer_id and self.customer_id.email and self.env.user.email:
            template = self.env.ref(
                "ak_library_search_domain.email_template_book_reservation",
                raise_if_not_found=False
            )
            if not template:
                raise ValidationError(
                    _("Mail template not found")
                )
            return {
                'name': _('Compose Email'),
                'type': 'ir.actions.act_window',
                'res_model': 'mail.compose.message',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_template_id': template.id,
                    'default_model': 'book.reservation',
                    'default_res_ids': [self.id],
                    'default_partner_ids': [self.customer_id.id],
                    'default_use_template': True,
                },
            }
        else:
            raise ValidationError(
                _("Customer's or Current User's Email-id not set yet")
            )
