# -- coding: utf-8 --
import json

from cffi import error
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', csrf=False) #library
    def xlsx_reports(self, model, option, output_format, report_name, token = 'ads'):
        """ Return data to python file passed from the javascript """
        session_unique_id = request.session.uid
        report_object = request.env['library.checkout'].with_user(session_unique_id)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response =request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'),(
                        'Content-Disposition',
                        content_disposition(f"{report_name}.xlsx")
                    )]
                )
                report_object.add_xlsx_action(options,response)
                response.set_cookie('fileToken',token)
                return response
        except Exception:
            error = {
                'code': 200,
                'message': 'Odoo Server Error'
            }
            return request.make_response(html_escape(json.dumps(error)))
