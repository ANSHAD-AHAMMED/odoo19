# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, Command
from datetime import timedelta, date

from odoo.exceptions import UserError


class LibraryCheckout(models.Model):
    _name = "library.checkout"
    _description = "Library Checkout"
    _rec_name = 'sequence_number'

    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one("res.users", string="User")
    book_id = fields.Many2one("library.book", string="Book")
    author_id = fields.Many2one("library.author", string="Author")

    checkout_line_ids = fields.One2many("library.checkout.line", "checkout_id", string="Books")

    phone_number = fields.Char(string="Phone Number", related="partner_id.phone")
    late_return_warning_text = fields.Char(string='Customer have many late returns',
                                           compute='late_returns_warning_text')

    penalty = fields.Float(string="Penalty", compute="_compute_penalty")
    invoice_amount = fields.Float(string="Invoice Amount", compute='_compute_invoice_data')

    return_date = fields.Datetime(string="Return Date")
    checkout_date = fields.Datetime(string="Available From")

    reminder_sent = fields.Boolean(default=False)
    overdue_sent = fields.Boolean(default=False)
    is_late = fields.Boolean(compute='_compute_is_late', store=True)
    is_paid = fields.Boolean(default=False)

    partner_late_count = fields.Integer(related="partner_id.late_count", store=True)
    invoice_count = fields.Integer(string="Invoice Count", compute='_compute_invoice_data')

    due_date = fields.Datetime(
        string="Due date",
        help="Validity of the order, after that you will not able to sign & pay the quotation.",
        compute='_compute_due_date',
        store=True)

    sequence_number = fields.Char(
        string="Reference Number",
        default=lambda self: _('New'),
        readonly=True, copy=False,
        help="Reference Number of the book")

    late_days = fields.Integer(compute="_compute_is_late", store=True)

    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('check_out', 'Check Out'),
            ('returned', 'Returned'),
            ('over_due', 'Over Due'),
            ('cancel', 'Cancel'),
        ],
        default='new',
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_warning(self):
        """ Show warning if partner have many late return """
        if not self.partner_id:
            return
        max_late_returns = int(self.env['ir.config_parameter'].sudo().get_param(
            'library_management.max_late_returns', default=1
        ))

        warning_limit = max_late_returns - 1
        if self.partner_late_count >= warning_limit:
            return {
                'warning': {
                    'title': "Warning",
                    'message': "this customer is about to reach late return limit",
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        """ Create reference number for the book """
        for vals in vals_list:
            if vals.get('sequence_number', _("New")) == _("New"):
                vals['sequence_number'] = self.env['ir.sequence'].next_by_code('library.checkout')
        return super().create(vals_list)

    @api.depends('checkout_date')
    def _compute_due_date(self):
        """ Compute due date for the book """
        days = int(self.env['ir.config_parameter'].sudo().get_param(
            'library_management.max_borrow_days', default=10
        ))
        for record in self:
            if record.checkout_date:
                record.due_date = record.checkout_date + timedelta(days=days)

    def confirm_checkout(self):
        """ Confirm the checkout """
        for record in self:
            if record.checkout_line_ids:
                """ To trigger this 2 functions in res.partner """
                record.partner_id._compute_book_count
                record.partner_id._compute_late_count

                if record.state == "cancel":
                    raise UserError("Cancelled book can't be checkout")

                max_late_returns = int(
                    self.env['ir.config_parameter'].sudo().get_param(
                        'library_management.max_late_returns', default=1
                    )
                )

                if record.partner_late_count >= max_late_returns:
                    raise UserError("partner late count is reached")

                partner = record.partner_id

                """ Show UserError if the user have any overdue """
                existing_books = sum(
                    len(r.checkout_line_ids)
                    for r in self.search([
                        ('partner_id', '=', partner.id),
                        ('state', '=', 'check_out')
                    ])
                )

                # Books in current checkout
                current_books = len(record.checkout_line_ids)

                # Total
                total_books = existing_books + current_books

                #  Check overdue
                overdue = self.search_count([
                    ('partner_id', '=', partner.id),
                    ('state', '=', 'over_due')
                ])
                print("overdue=", overdue)

                if overdue > 0:
                    raise UserError("you have overdue books")

                if total_books > partner.borrow_limit:
                    raise UserError("borrow limit reached")

                record.checkout_date = fields.Datetime.now()
                record.state = 'check_out'

                for line in record.checkout_line_ids:
                    if line.book_id:
                        line.book_id.sudo().status = 'unavailable'
                        line.partner_id = record.partner_id

                books = record.checkout_line_ids.mapped('book_id')
                for book in books:
                    book.sudo().count += 1

            else:
                raise UserError("You need to add at least one book")
            return {
                'type': 'ir.actions.act_window',
                'name': 'Book Suggestions',
                'res_model': 'suggestion.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_book_id': books.ids,
                    'checkout_id': self.id
                }
            }

    def return_checkout(self):
        """ Return the book """
        for record in self:
            if record.state == "cancel":
                raise UserError("Cancelled book can't be returned")

            record._compute_penalty()
            record._compute_is_late()

            record.return_date = fields.Datetime.now()
            record.state = 'returned'

            invoice_lines = []

            for line in record.checkout_line_ids:
                if not line.book_id or not line.book_id.product_id:
                    raise UserError("product not found in book")

                invoice_lines.append(Command.create({
                    'product_id': line.book_id.product_id.id,
                    'name': line.book_id.name,
                    'quantity': 1,
                    # 'product_uom_qty': 1,
                    'price_unit': line.book_id.price,
                }))
            if record.penalty > 0:
                invoice_lines.append(Command.create({
                    'name': 'Late return Penalty',
                    'quantity': 1,
                    'price_unit': record.penalty,
                }))

            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.partner_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_lines,
                'checkout_id': record.id,
            })

            invoice.action_post()
        return True

    def cancel_checkout(self):
        """Cancel function for the checkout"""
        for record in self:
            if record.state == "cancel":
                raise UserError("Cancelled property can't be cancel again")

            record.return_date = fields.Datetime.now()
            record.state = 'cancel'

            for line in record.checkout_line_ids:
                if line.book_id:
                    line.book_id.sudo().status = 'available'

    @api.depends('return_date', 'due_date')
    def _compute_is_late(self):
        """ Calculate late days """
        for rec in self:
            rec.is_late = False
            rec.late_days = 0

            if rec.return_date and rec.due_date:
                delay = (rec.return_date - rec.due_date).days
                if delay > 0:
                    rec.is_late = True
                    rec.late_days = delay

    @api.depends('return_date', 'due_date')
    def _compute_penalty(self):
        """ Compute penalty if the user not returned the book correct time """
        for record in self:
            record.penalty = 0

            if record.return_date and record.due_date:
                delay = record.return_date - record.due_date

                if hasattr(delay, 'total_seconds'):
                    delay_seconds = delay.total_seconds()

                    if delay_seconds > 0:
                        penalty_per_hour = float(
                            self.env['ir.config_parameter'].sudo().get_param(
                                'library_management.penalty_per_hour', default=1
                            )
                        )
                        delay_hours = delay_seconds / 3600
                        record.penalty = penalty_per_hour * delay_hours

    def send_due_notifications(self):
        """ To send email for due date reminders and overdue reminders """
        today = date.today()

        reminder_days = int(self.env['ir.config_parameter'].sudo().get_param(
            'library_management.reminder_days', default=2
        ))

        checkouts = self.search([('state', '=', 'check_out')])

        for rec in checkouts:

            if not rec.due_date:
                continue

            due_date = rec.due_date.date()

            # Reminder BEFORE due date
            if not rec.reminder_sent and due_date == today + timedelta(days=reminder_days):
                template = self.env.ref('library_management.email_template_reminder')
                print("template=", template)
                template.send_mail(rec.id, force_send=True)
                rec.reminder_sent = True
                print("reminder_send=", rec.reminder_sent)

            # Overdue
            if not rec.overdue_sent and due_date < today:
                template = self.env.ref('library_management.email_template_overdue')
                template.send_mail(rec.id, force_send=True)
                rec.overdue_sent = True
                rec.state = 'over_due'
                print("overdue_sent=", rec.overdue_sent)

    def _compute_invoice_data(self):
        """ Calculate invoice data """
        for record in self:
            invoice = self.env['account.move'].search([
                ('checkout_id', '=', record.id),
                ('move_type', '=', 'out_invoice'),
            ])

            record.invoice_count = len(invoice)
            record.invoice_amount = sum(invoice.mapped('amount_total'))

    def action_view_invoice_checkout(self):
        """ View checkout invoice from stat button """
        self.ensure_one()
        invoice = self.env['account.move'].search([
            ('checkout_id', '=', self.id),
            ('move_type', '=', 'out_invoice'),
        ])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
    