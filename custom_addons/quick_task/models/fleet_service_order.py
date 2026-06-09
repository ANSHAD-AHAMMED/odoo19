# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FleetServiceOrder(models.Model):
    _name = "fleet.service.order"
    _description = "Fleet Service Order"

    name = fields.Char(string="Name", default=lambda self: _('New'), readonly=True, copy=False, help="Reference Number of the book")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    technician_id = fields.Many2one('hr.employee', string="Technician")
    type_ids = fields.Many2many('checklist.type', string="Types")
    service_date = fields.Datetime(string="Service Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')
    ],default="draft", string="Status")

    parts_total = fields.Float(string="Total Parts", compute="_compute_parts_total", store=True)
    labour_cost = fields.Float(string="Labour Cost")
    grand_total = fields.Float(string="Grand Total", compute="_compute_grand_total", store=True)
    check_list_progress = fields.Float(string="Check List Progress", compute="_compute_check_list_progress", store=True)

    part_ids = fields.One2many('fleet.service.order.part', inverse_name="order_id", string="Part")
    checklist_ids = fields.One2many('fleet.service.order.checklist',inverse_name="order_id", string="Checklist")

    @api.onchange('state')
    def state_confirm(self):
        print('state:',self.state)
        if self.state == 'confirmed':
            if not self.part_ids:
                raise ValidationError('at least one part_ids line must exist.')

        if self.state == 'in_progress':
            if not self.technician_id:
                raise ValidationError('technician_id must be set.')

        if self._origin.state == 'done':
            if self.state == 'cancel':
                raise ValidationError('you cannot cancel.')

    @api.depends('checklist_ids')
    def _compute_check_list_progress(self):
        done = 0
        total = 0
        for part in self.checklist_ids:
            total = total + 1
            if part.is_done:
                done = done+1
        print('done:',done)
        print('total:',total)
        if done > 0 and total > 0:
            progress = done / total * 100
            self.write({'check_list_progress': progress if progress > 0 else 0})


    @api.depends('parts_total', 'labour_cost')
    def _compute_grand_total(self):
        total = self.parts_total + self.labour_cost
        self.write({'grand_total': total})

    @api.depends('part_ids')
    def _compute_parts_total(self):
        print('hi')
        parts=self.part_ids
        print(parts)
        total_amount = 0
        for part in parts:
            total = part.unit_price * part.quantity
            total_amount = total_amount + total


        self.write({'parts_total': total_amount})

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a new book """

        for vals in vals_list:
            # """Automatically generate a reference number for new books."""
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('fleet.service.order')

        return super().create(vals_list)