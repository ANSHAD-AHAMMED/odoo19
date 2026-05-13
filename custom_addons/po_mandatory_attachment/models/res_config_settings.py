# -*- coding: utf-8 -*-
from odoo import fields, models

class ResSettings(models.TransientModel):
    _inherit = "res.config.settings"

    require_attachment_on_purchase_order_confirmation = fields.Boolean(
        string="Require Attachment On Purchase Order Confirmation",
        config_parameter='po_mandatory_attachment.require_attachment_on_purchase_order_confirmation',
    )