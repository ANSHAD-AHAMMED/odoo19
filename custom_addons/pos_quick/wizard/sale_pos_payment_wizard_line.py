
from odoo import models, fields, api, _

class SalePosPaymentWizardLine(models.TransientModel):
    _name = 'sale.pos.payment.wizard.line'
    _description = 'Counter Payment Line'

    wizard_id = fields.Many2one('sale.pos.payment.wizard',string='Wizard',required=True,ondelete='cascade',)
    payment_method_id = fields.Many2one('pos.payment.method',string='Payment Method',required=True)
    amount = fields.Monetary(string='Amount',currency_field='currency_id',default=0.0,)
    currency_id = fields.Many2one(related='wizard_id.currency_id')
