from odoo import api, fields, models, tools
from odoo.addons.account.models.account_move import PAYMENT_STATE_SELECTION
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning

from functools import lru_cache


class AccountInvoiceReport(models.Model):
    _inherit="account.invoice.report"
    _name = "report.formato_report.report_journal_entries"
    _description = "Libro de Compras Report"


    @property
    def query(self):
        return '''
            select extract(year from move.invoice_date)||''||extract(month from move.invoice_date)||move.id as codigo,
            doc.code||' - '||doc.name as "tipo documento",
            move.name numero,
            move.invoice_date fecha,
            move.ref nombre,
            move.amount_untaxed as "importe libre impuesto",
            move.amount_tax impuesto,
            move.amount_total total
            from account_move move
            inner join l10n_latam_document_type doc
            	on move.l10n_latam_document_type_id = doc.id
            where move.invoice_date is not Null
            order by move.invoice_date desc
            ;
        '''
    @api.model
    def obtener_datos(self,docids, data=None):
        invoices = self.env['account.move'].browse(docids)
        self._cr.execute(self.query)
        query_results = self._cr.dictfetchall()

        report_values={
            'docs':invoices,
            'query_results':query_results,
        }
        return report_values
        

    