from odoo import fields, models, _, api
from odoo.exceptions import ValidationError, UserError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"

    name = fields.Char(string="Name", default=lambda self: _('New'), readonly=True, copy=False, help="Reference Number of the book")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    doctor_ids = fields.One2many('hr.employee', 'appointment_id', string="Doctor", compute='_compute_doctor_ids')
    department_id = fields.Many2one('hospital.department', string="Department")
    appointment_datetime = fields.Datetime(string="Appointment Date")
    consultation_fee = fields.Float(string="Consultation Fee")
    symptoms = fields.Text(string="Symptoms")
    diagnosis = fields.Text(string="Diagnosis")
    prescription_ids = fields.One2many('hospital.prescription.line', 'appointment_id', string="Prescriptions")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('consultation', 'Consultation'),
        ('completed', 'Completed'),
        ('cancel', 'Cancelled'),
    ])
    medicine_total = fields.Float(string="Medicine Total", compute='_compute_medicine_total', store=True)
    total_bill = fields.Float(string="Total Bill", compute='_compute_total_bill', store=True)


    @api.model_create_multi
    def create(self, vals_list):
        """ Create a new book """

        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')

            self.multiple_doctor_records()
            self.multiple_patient_records()

        return super().create(vals_list)

    @api.onchange('department_id')
    def _compute_doctor_ids(self):
        if self.department_id:
            person = self.department_id.doctor_ids.ids
            doc = self.env['hr.employee'].search([
                ('is_doctor', '=', True),
                ('is_available', '=', True),
            ])
            self.write({
                'doctor_ids': person in doc
            })
        else:
            doc = self.env['hr.employee'].search([
                ('is_doctor', '=', True),
                ('is_available', '=', True),
            ])
            self.write({
                'doctor_ids': doc
            })

    @api.onchange('doctor_id')
    def multiple_doctor_records(self):
        multiple_doctor_appointment = self.env['hospital.appointment'].search([
            ('doctor_id', '=', self.doctor_id),
            ('appointment_datetime', '=', self.appointment_datetime),
        ])

        if multiple_doctor_appointment:
            raise ValidationError("This doctor have a same time appointment")

    @api.onchange('patient_id')
    def multiple_patient_records(self):
        multiple_appointment = self.env['hospital.appointment'].search([
            ('patient_id', '=', self.patient_id),
            ('appointment_datetime', '=', self.appointment_datetime),
        ])

        if multiple_appointment:
            raise ValidationError("This patient have a same time appointment")

    @api.onchange('appointment_datetime')
    def past_appointment_time(self):
        today = fields.Datetime.today()
        self.multiple_patient_records()
        self.multiple_doctor_records()
        if self.appointment_datetime:
            if self.appointment_datetime.day < today.day:
                raise ValidationError("This appointment date is in the past")

    def schedule_appointment(self):
        if self.patient_id and self.doctor_id:
            self.write({'state': 'scheduled'})
        else:
            raise UserError("No patient to selected")

    def start_consultation(self):
        self.write({'state': 'consultation'})

    def complete_consultation(self):
        if self.diagnosis and self.prescription_ids:
            self.write({'state': 'completed'})
        else:
            raise UserError("No diagnosis or prescription")

    @api.ondelete(at_uninstall=False)
    def delete_appointment(self):
        for record in self:
            if record.state not in ('cancelled', 'draft'):
                raise UserError("state must be 'cancelled' or 'draft' to delete appointment")

        return True

    @api.depends('prescription_ids')
    def _compute_medicine_total(self):
        total = 0

        if self.prescription_ids:
            for record in self.prescription_ids:
                count = 0
                for rec in self.prescription_ids:
                    if rec.product_id == record.product_id:
                        count += 1
                    if count == 2:
                        raise UserError(_('The product id is same'))

        for t in self.prescription_ids:
            if t:
                sum_total = t.quantity * t.unit_price
                total = total + sum_total
        self.write({'medicine_total': total if total else 0})

    @api.depends('consultation_fee','medicine_total')
    def _compute_total_bill(self):
        total = self.consultation_fee + self.medicine_total
        self.write({'total_bill': total if total else 0})