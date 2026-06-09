# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class CRMLead(models.Model):
    _inherit = "crm.lead"

    lead_meetings = fields.Integer(string="Meetings", compute="_compute_lead_meetings")

    @api.depends('lead_meetings')
    def _compute_lead_meetings(self):
        meetings = self.env['calendar.event'].search_count([('res_id', 'in', self.id)])
        self.write({'lead_meetings': meetings if meetings else 0})

    def write(self, vals_list):
        lead = super().write(vals_list)

        if self.stage_id.is_won:
            meetings = self.env['calendar.event'].search([('res_id', 'in', self.id)])
            if len(meetings) <= 0:
                if not self.env.user.has_group('prevent_crm_lead.crm_manager_group'):
                    raise ValidationError("This Lead has no meetings!")

        return lead
