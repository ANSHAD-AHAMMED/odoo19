from odoo import fields, models, api

class HospitalPrescriptionLine(models.Model):
    _name = "hospital.prescription.line"
    _description = "Hospital Prescription Line"

    appointment_id = fields.Many2one('hospital.appointment', string="Hospital Appointment")
    product_id = fields.Many2one('product.product', string="Product")
    dosage = fields.Char(string="Dosage")
    days = fields.Integer(string="Days")
    quantity = fields.Integer(string="Quantity", default=1)
    unit_price = fields.Float(string="Unit Price", related="product_id.lst_price")
