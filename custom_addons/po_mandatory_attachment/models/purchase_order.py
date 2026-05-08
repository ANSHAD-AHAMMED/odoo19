# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        """ check attached file type if attachment is mandatory """
        is_attachment = (self.env['ir.config_parameter'].sudo().get_param(
            'po_mandatory_attachment.require_attachment_on_purchase_order_confirmation', default=False
        ))

        if is_attachment:
            print('is_attachment=', is_attachment)

            attachment = self.env['ir.attachment'].search([
                ('res_model', '=', 'purchase.order'),
                ('res_id', '=', self.id)
            ])

            print('attachment=',attachment)

            if attachment:
                if '.pdf' in attachment.name or '.jpeg' in attachment.name or '.png' in attachment.name or 'jpg' in attachment.name:
                    print('attachment=',attachment.name)
                    return super().button_confirm()
                else:
                    raise UserError('only image and pdf are allowed')
            if not attachment:
                print('hi')
                raise UserError('attachment is mandatory')

        else:
            print('is_attachment=', is_attachment)
            return super().button_confirm()

