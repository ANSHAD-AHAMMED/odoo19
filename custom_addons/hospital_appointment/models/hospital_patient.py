from odoo import fields, models, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    name = fields.Char(string="Patient")
    date_of_birth = fields.Datetime(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other")
    ])
    blood_group = fields.Selection([
        ("a+","A+"),
        ("b+", "B+"),
        ("ab+", "AB+"),
        ("o+", "O+"),
        ("a-", "A-"),
        ("b-", "B-"),
        ("ab-", "AB-"),
        ("o-", "O-"),
    ])
    mobile =fields.Char(string="Mobile")
    department_id = fields.Many2one('hospital.department', string="Department")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    state = fields.Selection([
        ("draft", "Draft"),
        ('archived', "Archived"),
        ('discharged', "Discharged"),
    ],default="draft", string="Status", compute="_compute_status")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count", store=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        count = 0
        for patient in self.appointment_ids:
            count = count + 1

        self.write({'appointment_count': count if count else 0})

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Datetime.today()
        for record in self:
            if record.date_of_birth:
                age = today.year - record.date_of_birth.year

                record.write({'age': age if age else 0})

            else:
                record.write({'age': 0})

    @api.depends('appointment_ids')
    def _compute_status(self):
        discharge = 0
        for status in self.appointment_ids:
            if status.state != 'completed':
                discharge = discharge + 1
                if discharge >= 1:
                    self.write({'state': 'draft'})
                    break
            else:
                self.write({'state': 'discharged'})
