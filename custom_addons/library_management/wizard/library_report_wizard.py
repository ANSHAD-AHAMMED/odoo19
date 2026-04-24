# -- coding: utf-8 --
import io
import json

from pydantic import color

import xlsxwriter
from odoo import fields, models

class LibraryReportWizard(models.TransientModel):
    _name = 'library.report.wizard'
    _description = 'Library Report Wizard'

    partner_id = fields.Many2one('res.partner', string='Member')
    checkout_date = fields.Datetime(string='Checkout Date')
    return_date = fields.Datetime(string='Return Date')
    book_id = fields.Many2one('library.book', string='Book')
    tag_id = fields.Many2one('library.tag', string='Tag')
    genre_id = fields.Many2one('library.genre', string='Genre')
    sort_by = fields.Selection([
        ('lc.checkout_date', 'Checkout Date'),
        ('lc.due_date', 'Due Date'),
    ], string='Sort By', default='lc.checkout_date')

    sort_order_by = fields.Selection([
        ('ASC', 'Ascending'),
        ('DESC', 'Descending'),
    ])

    def _fetch_report_data(self):
        """ Collect report data using psql query and filters and sorting are applied dynamically. """
        query = """
            SELECT
                lc.sequence_number               AS reference_id,
                rp.name                          AS partner_id,
                lb.name                          AS book_name,
                la.name                          AS author,
                lc.checkout_date                 AS checkout_date,
                lc.return_date                   AS return_date,
                lc.due_date                      AS due_date,
                lt.name                          AS tag,
                lg.name                          AS genre
            FROM library_checkout lc
            JOIN res_partner rp       ON rp.id = lc.partner_id
            JOIN library_checkout_line lcl ON lcl.checkout_id = lc.id
            JOIN library_book lb      ON lb.id = lcl.book_id
            LEFT JOIN library_author la   ON la.id = lb.author_id
            LEFT JOIN library_genre lg   ON lg.id = lb.genre_id
            LEFT JOIN library_book_library_tag_rel btr ON btr.library_book_id = lb.id
            LEFT JOIN library_tag lt     ON lt.id = btr.library_tag_id
            WHERE 1=1
        """
        values = []

        if self.partner_id:
            query += " AND lc.partner_id = %s"
            values.append(self.partner_id.id)

        if self.checkout_date:
            query += " AND lc.checkout_date >= %s"
            values.append(self.checkout_date)

        if self.return_date:
            query += " AND lc.return_date <= %s"
            values.append(self.return_date)

        if self.book_id:
            query += " AND lcl.book_id = %s"
            values.append(self.book_id.id)

        if self.tag_id:
            query += " AND lt.id = %s"
            values.append(self.tag_id.id)

        if self.genre_id:
            query += " AND lg.id = %s"
            values.append(self.genre_id.id)

        query += """
            GROUP BY
                lc.sequence_number,
                rp.name,
                lb.name,
                la.name,
                lc.checkout_date,
                lc.return_date,
                lc.due_date,
                lt.name,
                lg.name
        """
        # print('values=', values)
        # print('query=', query)
        order = self.sort_order_by or 'ASC'
        sort = self.sort_by
        query += f" ORDER BY {sort} {order} NULLS LAST"

        value = self.env.cr.execute(query, values)
        rows = self.env.cr.dictfetchall()
        return rows

    def add_report_action(self):
        """ print the report data """
        lines = self._fetch_report_data()
        data = {
            'lines': lines,
            'partner_name': self.partner_id.name if self.partner_id else None,
            'book_name': self.book_id.name if self.book_id else None,
            'tag_name': self.tag_id.name if self.tag_id else None,
            'genre_name': self.genre_id.name if self.genre_id else None,
        }
        return self.env.ref(
            'library_management.action_library_report_print'
        ).report_action(self, data=data)

    def generate_xlsx_report(self, options, response):
        """ Generate an xlsx report """
        lines = self._fetch_report_data()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Library Report')

        head = workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': 20,
            'bg_color':'#3333ff',
            'color': 'white',
            'border': 2
        })
        col_head = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 12,
            'bg_color': '#6666ff',
            'color': 'white',
            'border': 1
        })
        filter = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 12,
            'bg_color': '#944dff',
            'color': 'white',
            'border': 1
        })
        cell_format = workbook.add_format({
            'align': 'center',
            'font_size': 12,
        })

        sheet.merge_range('A1:I1', 'Library Management Report', head)
        sheet.set_row(0,30)

        headers = ['Reference ID']

        if not options['partner_id']:
            headers.append('Member')

        if not options['book_id']:
            headers.append('Book')

        headers.append('Author')
        headers.append('Checkout Date')
        headers.append('Return Date')
        headers.append('Due Date')

        if not options['tag_id']:
            headers.append('Tag')

        if not options['genre_id']:
            headers.append('Genre')

        col_width = [30, 30, 30, 30, 30, 30, 30, 30, 30]
        start_table = 2
        data = 0
        row = 0
        if options['partner_id']:
            data += 1

        if options['book_id']:
            data += 1

        if options['tag_id']:
            data += 1

        if options['genre_id']:
            data += 1

        for col,(headers,width) in enumerate(zip(headers, col_width)):

            if data > 0:
                print('data=', data)
                for i in range(data):
                    print("hi")
                    if options['partner_id']:
                        print("first if")
                        row += 1
                        sheet.write(row, 0, "Partner",filter)
                        sheet.write(row, 1, self.partner_id.name, filter)

                    if options['book_id']:
                        row += 1
                        sheet.write(row, 0, "Book", filter)
                        sheet.write(row, 1, self.book_id.name, filter)

                    if options['tag_id']:
                        row += 1
                        sheet.write(row, 0, "Tag",filter)
                        sheet.write(row, 1, self.tag_id.name, filter)

                    if options['genre_id']:
                        row += 1
                        sheet.write(row, 0, "Genre", filter)
                        sheet.write(row, 1, self.genre_id.name, filter)

                    data = 0
                    start_table = row + 2
                    break

            # row += 2
            sheet.write(start_table, col, headers, col_head)
            sheet.set_column(col, col, width)


        start_table += 1

        # row_ids = start_table
        for row_ids, record in enumerate(lines, start = start_table):
            column = 0


            sheet.write(row_ids, column, record.get('reference_id') or '', cell_format)

            if not options['partner_id']:
                print("partner id=",record.get('partner_id'))
                column += 1
                sheet.write(row_ids, column, record.get('partner_id') or '', cell_format)

            if not options['book_id']:
                print("book name=",record.get('book_name'))
                column += 1
                sheet.write(row_ids, column, record.get('book_name') or '', cell_format)

            column += 1
            print('author')
            sheet.write(row_ids, column, record.get('author') or '', cell_format)


            checkout = record.get('checkout_date')
            return_d = record.get('return_date')
            due_d = record.get('due_date')

            if not options['checkout_date']:
                print('checkout date')
                column += 1
                sheet.write(row_ids, column, str(checkout)[:10] if checkout else '', cell_format)

            if not options['return_date']:
                print('return date')
                column += 1
                sheet.write(row_ids, column, str(return_d)[:10] if return_d else '', cell_format)

            column += 1
            print('due_date')
            sheet.write(row_ids, column, str(due_d)[:10] if due_d else '', cell_format)

            if not options['tag_id']:
                print('tag id')
                column += 1
                sheet.write(row_ids, column, record.get('tag') or '', cell_format)

            if not options['genre_id']:
                print('genre id')
                column += 1
                sheet.write(row_ids, column, record.get('genre') or '', cell_format)

            print('===================================================================')

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def add_xlsx_action(self):
        """ XLSX actions send data to js """
        data = {
            'partner_id': self.partner_id.id or False,
            'checkout_date': self.checkout_date or False,
            'return_date': self.return_date or False,
            'book_id': self.book_id.id or False,
            'tag_id': self.tag_id.id or False,
            'genre_id': self.genre_id.id or False,
            'sort_by': self.sort_by or 'lc.checkout_date',
            'sort_order_by': self.sort_order_by or 'ASC',
        }
        return {
            'type': 'ir.actions.report',
            'data':{
                'options': json.dumps(data),
                'output_format': 'xlsx',
                'report_name': 'Library Management Report',
            },
            'report_type': 'excel',
        }
