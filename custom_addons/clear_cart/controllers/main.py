# -*- coding: utf-8 -*-
import odoo.http as http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from werkzeug.utils import redirect


class WebsiteTopSelling(Website):
    @http.route('/shop/cart/clear_cart', type='http', auth='public', website=True, csrf=False)
    def clear_full_cart(self):
        """ clear cart """
        request.cart.order_line.unlink()
        return redirect("/shop/cart")
