from . import properties, property_types, property_tags, property_offer, user_model_inheritance, abin_tasks


# @api.model
# def create(self, vals):
#     if 'borrow_limit' not in vals:
#         limit = int(self.env['ir.config_parameter'].sudo().get_param(
#             'library_management.maximum_borrow_books', default=1
#         ))
#         vals['borrow_limit'] = limit
#     return super().create(vals)