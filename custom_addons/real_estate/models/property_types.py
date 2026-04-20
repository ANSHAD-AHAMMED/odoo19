from odoo import fields,models, api

class property_types(models.Model):
    _name = 'property_types'
    _description = 'property type for specify the property'
    _order = "sequence desc"

    name = fields.Char(string='property_type')
    line_ids = fields.One2many("properties", "property_type")

    sequence = fields.Integer(string="Properties", compute="_compute_property_count", store=True)

    # TO COUNT THE PROPERTY IN A PROPERTY_TYPE. IF A PROPERTY_TYPE HAVE MORE PROPERTY, IT WILL BE ON THE TOP OF THE LIST
    @api.depends('line_ids')
    def _compute_property_count(self):
        for record in self:
            record.sequence = len(record.line_ids)


    # TO COUNT OFFERS IN A PROPERTY TYPES
    offer_count = fields.Integer( compute="_compute_offer_count")

    @api.depends("line_ids.offer_id")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.mapped("line_ids.offer_id"))

    def action_property_types_offers(self):
        self.ensure_one()

        return {
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'property.offer',
            'view_mode': 'list,form',
            'domain': [('properties_id.property_type', '=', self.id)],
            'target': 'current',
        }