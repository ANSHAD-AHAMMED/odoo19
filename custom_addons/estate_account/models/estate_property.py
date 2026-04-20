from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "properties"

    def sold(self):
        for record in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id':record.partner_id.id,
                'invoice_date':fields.Date.today(),
                'invoice_line_ids':[
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),
                    Command.create({
                        'name': 'Administrate Fee',
                        'quantity': 1,
                        'price_unit': 100,
                    }),
            ],
            })
            return super().sold()