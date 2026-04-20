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

    def _fetch_report_data(self):
        """
        Fetch report data using raw PSQL query.
        Filters and sorting are applied dynamically.
        """
        query = """
            SELECT
                lc.sequence_number               AS reference_id,
                rp.name                          AS member_name,
                lb.name                          AS book_name,
                la.name                          AS author,
                lc.checkout_date                 AS checkout_date,
                lc.return_date                   AS return_date,
                lc.due_date                      AS due_date,
                STRING_AGG(DISTINCT lt.name, ', ') AS category,
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
        params = []

        if self.partner_id:
            query += " AND lc.partner_id = %s"
            params.append(self.partner_id.id)

        if self.checkout_date:
            query += " AND lc.checkout_date >= %s"
            params.append(self.checkout_date)

        if self.return_date:
            query += " AND lc.return_date <= %s"
            params.append(self.return_date)

        if self.book_id:
            query += " AND lcl.book_id = %s"
            params.append(self.book_id.id)

        if self.category_id:
            query += " AND lt.id = %s"
            params.append(self.category_id.id)

        if self.genre_id:
            query += " AND lg.id = %s"
            params.append(self.genre_id.id)

        # GROUP BY before ORDER BY
        query += """
            GROUP BY
                lc.sequence_number,
                rp.name,
                lb.name,
                la.name,
                lc.checkout_date,
                lc.return_date,
                lc.due_date,
                lg.name
        """

        sort_col = self.sort_by or 'lc.checkout_date'
        query += f" ORDER BY {sort_col} ASC NULLS LAST"

        self.env.cr.execute(query, params)
        rows = self.env.cr.dictfetchall()
        return rows

    def add_report_action(self):
        lines = self._fetch_report_data()
        data = {'lines': lines}
        return self.env.ref(
            'library_management.action_library_report_print'
        ).report_action(self, data=data)
# from odoo import fields, models
#
# class LibraryManagementReport(models.TransientModel):
#     _name = 'library.management.report'
#     _description = 'Library Management Report'
#
#     partner_id = fields.Many2one('res.partner', string="Customer")
#     checkout_date = fields.Datetime(string="Order Date")
#     return_date = fields.Datetime(string="Order Date")
#     book_id = fields.Many2one('library.book', string="Book")
#     tag_id = fields.Many2one('library.tag', string="Tag")
#     genre_id = fields.Many2one('library.genre', string="Genre")
#
#
#     def action_report_library_managemet(self):
#         query = """ SELECT pr.name,sc.sequence_number from library_checkout as lc
#         INNER JOIN library_book as b on b.book_id = b.id
#         INNER JOIN library_tag as t on t.tag_id = t.id
#         INNER JOIN library_genre as g on g.genre_id = g.id
#         INNER JOIN res_partner as pr on pr.partner_id = pr.id
#         INNER JOIN library_checkout as sc on sc.book_id = sc.id
#         """

    # ===================================================================
    #     domain = []
    #
    #     if self.partner_id:
    #         domain.append(('partner_id', '=', self.partner_id.id))
    #     if self.checkout_date:
    #         domain.append(('checkout_date', '=', self.checkout_date))
    #     if self.return_date:
    #         domain.append(('return_date', '=', self.return_date))
    #     if self.book_id:
    #         domain.append(('book_id', '=', self.book_id.id))
    #     if self.tag_id:
    #         domain.append(('tag_id', '=', self.tag_id.id))
    #     if self.genre_id:
    #         domain.append(('genre_id', '=', self.genre_id.id))
    #
    #     report = self.env['library.checkout'].search(domain)
    #     print('report', report)
    #     data = {
    #         'form':self.read()[0],
    #         'report':report.ids,
    #     }
    #     return self.env.ref('library_management.action_report_library_managemet').report_action(self, data = data)
    #