# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class WebsiteProduct(http.Controller):

   @http.route('/get_product_categories', auth="public", type='jsonrpc',website=True)
   def get_product_category(self):
       """Get the website categories for the snippet."""
       # public_categs = request.env[
       #     'product.public.category'].sudo().search_read(
       #     [('parent_id', '=', False)], fields=['name', 'image_1920', 'id']
       # )

       public_categs = self.env[
           'library.book'].search_read([
           # ('status','=','available')
       ])
       print('public_categs=',public_categs)
       values = {
           'categories': public_categs,
       }
       print('values=',values)
       return values
