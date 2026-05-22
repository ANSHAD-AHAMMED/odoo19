# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    archive_project = fields.Boolean(
        String='Archive Project',
        config_parameter='auto_archive_stale_project.archive_project',
    )
