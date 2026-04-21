# -- coding: utf-8 --
from odoo import fields, models

class LibraryReportWizard(models.TransientModel):
    _name = 'library.report.wizard'
    _description = 'Library Report Wizard'

    partner_id = fields.Many2one('res.partner', string='Member')
    checkout_date = fields.Datetime(string='Checkout Date')
    return_date = fields.Datetime(string='Return Date')
    book_id = fields.Many2one('library.book', string='Book')
    category_id = fields.Many2one('library.tag', string='Category')
    genre_id = fields.Many2one('library.genre', string='Genre')
    sort_by = fields.Selection([
        ('lc.checkout_date', 'Checkout Date'),
        ('lc.checkout_due_date', 'Due Date'),
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

        if self.category_id:
            query += " AND lt.id = %s"
            values.append(self.category_id.id)

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

        abc = self.env.cr.execute(query, values)
        print('abc=', abc)
        rows = self.env.cr.dictfetchall()
        print('rows=', rows)
        return rows

    def add_report_action(self):
        """ print the report data """
        lines = self._fetch_report_data()
        print('lines=', lines)
        data = {'lines': lines}
        print('data=', data)
        return self.env.ref(
            'library_management.action_library_report_print'
        ).report_action(self, data=data)