from odoo import fields,models, api, Command
from odoo.exceptions import UserError
# from odoo.exceptions import UserError


class Properties(models.Model):
    _name = 'properties'
    _description = 'properties Model details'
    _order = "id desc"

    name = fields.Char(required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one("res.users", string="Seller")
    description = fields.Text()
    postal_code = fields.Char()
    date_availability = fields.Datetime(string="Available From",required=True, default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute='_compute_best_offer')
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area", default=1)
    garage = fields.Boolean()
    garden = fields.Boolean(string="Garden")
    garden_length = fields.Integer()
    garden_breadth = fields.Integer()
    garden_area= fields.Float(compute='_compute_total',inverse="_inverse_total")   #COMPUTE FUNCTION IS ALREADY READ_ONLY, IF WE ADD INVERSE FUNCTION, THEN WE CAN MANUALLY CHANGE VALUES
    active = fields.Boolean(default=False)
    tags = fields.Many2many('property_tags', string='Tags',)
    property_type = fields.Many2one('property_types', string="Property Type")
    offer_id = fields.One2many('property.offer', 'properties_id', string="Offer")
    image = fields.Image(string="Image ABC")
    sale_order_id=fields.Many2one('sale.order',string="Sale Order")


    #A SELECTION FIELD FOR GARDEN ORIENTATION
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')],
    )

    #COMPUTE AREA OF THE GARDEN
    @api.depends("garden_length", "garden_breadth")
    def _compute_total(self):
        for record in self:
            record.garden_area = record.garden_breadth * record.garden_length


    # def action_approve_loan(self):
    #     for rec in self:
    #         if rec.loan_amount <= 0:
    #             raise UserError("Loan amount must be greater than 0.")
    #
    #         rec.state = 'approved’

    #FOR MANUALLY ADDING THE GARDEN AREA, IT WILL AUTOMATICALLY CALCULATE THE LENGTH OF THE GARDEN
    def _inverse_total(self):
        for record in self:
            if record.garden_breadth > 0:
                record.garden_length = record.garden_area / record.garden_breadth

    #COMPUTING THE SELLING PRICE BASED ON THE OFFERS, OFFER VALUE WILL GET FROM 'offer_id', IT CONNECTED TO property_offer.py MODEL
    @api.depends("offer_id.price", "offer_id.status")
    def _compute_best_offer(self):
        for record in self:
            price=[o.price for o in record.offer_id if o.status !='reject'] #IT ONLY TAKE DATA FROM THE ACCEPTED OFFERS
            record.best_offer = max(price) if price else 0  #IT WILL SHOW MAXIMUM VALUE OF THE SELLING PRICE

    # loan_line_count = fields.Integer(
    #     string="Installments Count",
    #     compute="_compute_loan_line_count"
    # )
    #
    # def _compute_loan_line_count(self):
    #     for rec in self:
    #         rec.loan_line_count = len(rec.loan_line_ids)

    # STAGES
    state=fields.Selection(
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('cancel', 'Cancel'),
            ('sold', 'Sold')],
        default="new",
    )

    #CANCEL FUNCTION FOR IF WE CLICK THE BUTTON CANCEL IT WILL CANCEL, WE CANNOT SELL IT AGAIN
    def cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold property can't be cancelled")
            record.state = "cancel"
        return True

    # SOLD FUNCTION FOR IF WE CLICK THE BUTTON SOLD IT WILL SELL, WE CANNOT CANCEL IT AGAIN
    def sold(self):
        for record in self:
            if record.state == "cancel":
                raise UserError("Cancelled property can't be sold")
            record.state = "sold"

            # CHANGE THE PROPERTY INTO PRODUCT
            product = self.env['product.product'].create({'name': record.name})

            sale_order = self.env['sale.order'].create({
                'partner_id': self.partner_id.id,
                'order_line': [Command.create({
                    'product_id': product.id,
                    'name': record.name,
                    'product_uom_qty': 1,
                    'price_unit': record.selling_price,
                }), ]
            })
            sale_order.action_confirm()
        return True

    #ADDING THE CONSTRAINTS FOR CHECKING THE SELLING PRICE IS A POSITIVE VALUE
    _check_best_offer = models.Constraint(
        'CHECK(best_offer > 0)',
        'The selling price should be a Positive number.',
    )

    # ADDING THE CONSTRAINTS FOR CHECKING THE EXPECTED PRICE IS A POSITIVE VALUE
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price should be a Positive number.',
    )

    # CHECK SELLING PRICE LESS THAN 90% OF THE EXPECTED PRICE
    @api.constrains("expected_price","selling_price")
    def check_selling_offer_percentage(self):
        for record in self:
            if record.selling_price < (record.expected_price*0.9) and record.selling_price > 0:
                raise UserError("selling price at least 90% of the expected price")

    # PREVENT DELETION IF THE STAGES NOT IN NEW OR CANCEL
    @api.ondelete(at_uninstall=False)
    def _sold_cancel_delete(self):
        for record in self:
            if record.state != "new" and record.state != "cancel":
                raise UserError("You cannot delete a active property without cancelling it.")

    # NEW PROBLEM, OTHER THAN THE PROPERTY MODULE
    # TO GET DETAILS FROM A SALE ORDER (Customer Name, Customer Country, Customer Currency, Customer Total number of sale orders, Customer Total sale amount, Customer Product-wise purchase quantity, Customer Highest purchased product, Customer Least purchased product)
    def sale_order_details(self):
        for record in self:
            customer = record.sale_order_id.partner_id.name
            customer_id = record.sale_order_id.partner_id.id
            country = record.sale_order_id.partner_id.country_id.name
            currency = record.sale_order_id.partner_id.currency_id.name
            all_orders = self.env['sale.order'].search([
                ('partner_id','=',customer),
                ('state','in',['sale'])
            ])
            total_orders = len(all_orders)
            total_amount = sum(all_orders.mapped('amount_total'))

            sale_order_line = self.env['sale.order.line'].search([('order_id.partner_id','=',customer_id)])
            full_product = {}
            for i in sale_order_line:
                product = i.product_id.name
                full_product[product] = full_product.get(product, 0) + i.product_uom_qty



            print("customer name=",customer)
            print("country name=",country)
            print("currency=", currency)
            print("total sales order =", total_orders)
            print("total sales amount =", total_amount)
            print("product =", full_product)
            print('least quantity=',min(full_product, key=full_product.get))
            print('Highest quantity=', max(full_product, key=full_product.get))

    def action_cybrosys(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://www.cybrosys.com/",
            "target": "_blank", # IF I USE self INSTED OF _blank, IT WILL LOAD IN SAME TAB
        }
