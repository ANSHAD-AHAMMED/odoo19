# -- coding: utf-8 --
import json

from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', csrf=False)

    def xlsx_reports(self, options, output_format, report_name, **kwargs):
        """ Return data to python file passed from the js """
        # session_unique_id = request.session.uid
        # report_object = request.env['library.checkout'].with_user(session_unique_id)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'),
                             ('Content-Disposition',
                              content_disposition(f"{report_name}.xlsx")
                    )]
                )
                # wizard_id = options.get('model_id')
                wizard = request.env['library.report.wizard'].with_user(
                    request.session.uid
                ).create({
                    'partner_id': options.get('partner_id') or False,
                    'book_id': options.get('book_id') or False,
                    'tag_id': options.get('tag_id') or False,
                    'genre_id': options.get('genre_id') or False,
                    'checkout_date': options.get('checkout_date') or False,
                    'return_date': options.get('return_date') or False,
                    'sort_by': options.get('sort_by') or 'lc.checkout_date',
                    'sort_order_by': options.get('sort_order_by') or 'ASC',
                })
                wizard.generate_xlsx_report(options,response)
                response.set_cookie('fileToken',kwargs.get('token','token'))
                return response
        except Exception as e:
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': html_escape(str(e)),
            }
            return request.make_response(
                json.dumps(error),
                headers=[('Content-Type', 'application/json')],
            )
