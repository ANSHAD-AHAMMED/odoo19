from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one("res.users", string="Seller")
    properties_id = fields.Many2one("properties", string="Property")
    status = fields.Selection(
        [('accept','Accept'), ('reject','Reject')],
        string="Status",
        readonly=True,
    )
    offer_start_date = fields.Datetime(string="Available From", required=True, default=fields.Datetime.now)
    validity = fields.Integer(string="Validity")
    expiry_date = fields.Datetime(string="expiry_date", compute="_compute_total_offer_days", store=True)

    # CHECK THE OFFER PRICE IS GREATER THAN ZERO
    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer amount should be a Positive number.',
    )

    # from datetime import timedelta
    #
    # def action_generate_installments(self):
    #     for rec in self:
    #         if not rec.installment_count:
    #             raise UserError("Installment count must be greater than 0.")
    #
    #         installment_amount = rec.installment_amount or (rec.loan_amount / rec.installment_count)
    #
    #         lines = []
    #         date = rec.start_date or fields.Date.today()
    #
    #         for i in range(rec.installment_count):
    #             lines.append((0, 0, {
    #                 'loan_id': rec.id,
    #                 'date': date,
    #                 'amount': installment_amount,
    #                 'paid': False,
    #             }))
    #             date = date + timedelta(days=30)  # monthly approx
    #
    #         rec.loan_line_ids = lines
    #         rec.state = 'ongoing’

    # SET THE STAGE INTO OFFER ACCEPTED, IF A OFFER IS ACCEPTED
    def action_confirm(self):
        for record in self:
            if 'accept' in record.properties_id.offer_id.mapped('status'):
                raise UserError("An offer has already been accepted")
            record.properties_id.state = "offer_accepted"
            record.status = ("accept")
            record.properties_id.selling_price=record.price
            record.properties_id.partner_id = record.partner_id
        return True

    # SET THE STAGE INTO CANCEL, IF A OFFER IS CANCELLED
    def action_cancel(self):
        for record in self:
            record.status = ("reject")
        return True

    # paid_amount = fields.Float(
    #     string="Paid Amount",
    #     compute="_compute_paid_amount",
    #     store=True
    # )
    #
    # balance_amount = fields.Float(
    #     string="Balance Amount",
    #     compute="_compute_balance_amount",
    #     store=True
    # )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['properties'].browse(vals.get('properties_id'))

            if property_record.state=="sold":
                raise ValidationError("The property has already sold, you cannot add new offers")

            if property_record.state=="cancel":
                raise ValidationError("The property has already cancelled, you cannot add new offers")

            if 'accept' in property_record.offer_id.mapped('status'):
                raise ValidationError("An offer has already been accepted")

            # PREVENT ADDING OFFERS IF THE PRICE IS LESSER THAN PREVIOUS OFFERS
            if property_record.offer_id:
                max_offer = max(property_record.offer_id.mapped("price"))
                if vals.get('price') <= max_offer:
                    raise UserError("You can only add best offers, not lesser than previous offer price")
            property_record.state = "offer_received"

        return super(PropertyOffer, self).create(vals)

    # CALCULATE THE VALIDITY DATE OF THE OFFERS
    @api.depends("offer_start_date", "validity")
    def _compute_total_offer_days(self):
        for record in self:
            record.expiry_date = record.offer_start_date + relativedelta(days=record.validity)

    # @api.depends('loan_line_ids.paid', 'loan_line_ids.amount')
    # def _compute_paid_amount(self):
    #     for rec in self:
    #         rec.paid_amount = sum(
    #             line.amount for line in rec.loan_line_ids if line.paid
    #         )
    #
    # @api.depends('paid_amount', 'total_payable')
    # def _compute_balance_amount(self):
    #     for rec in self:
    #         rec.balance_amount = rec.total_payable - rec.paid_amount

    # TO PREVENT THE END DATE SET IN THE PAST
    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        for record in self:
            if record.expiry_date < fields.Datetime.today():
                raise ValidationError("The end date cannot be set in the past")
