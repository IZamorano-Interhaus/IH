from odoo import api, fields, models, tools
from odoo.addons.account.models.account_move import PAYMENT_STATE_SELECTION
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning

from functools import lru_cache


class AccountInvoiceReport(models.Model):
    _inherit ="account.invoice.report"
    _name = "report.libro_compras.report_journal_entries"
    _description = "Libro de Compras Report"
    
    _depends = {
        'account.move': [
            'name', 'state', 'move_type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_subtotal', 'price_total', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @property
    def table_query(self):
        return '''
            select  
            doc.code||' - '||doc.name as tipo_documento,
            count(doc.name) as Cantidad_Docs_x_Tipo,
            to_char(round(sum(amount_tax/0.19),0),'999,999,999') afecto,
            to_char(round(sum(amount_untaxed-(amount_tax/0.19)),0),'99,999,999') exento,
            to_char(sum(amount_tax),'999,999,999') Iva,
            to_char(sum(amount_total),'999,999,999') Total
            from account_move move
            inner join l10n_latam_document_type doc
            	on move.l10n_latam_document_type_id = doc.id
            group by doc.code||' - '||doc.name
            order by doc.code||' - '||doc.name asc
            '''       
    @api.model
    def _get_report_values(self, docids, data=None):
        # Obtener los registros de las facturas
        invoices = self.env['account.move'].browse(docids)
    
        # Realizar la consulta y obtener los resultados
        self._cr.execute(self.table_query)
        query_results = self._cr.dictfetchall()
        
        
    
       # Agregar los resultados de la consulta al diccionario de valores del informe
        report_values = {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'invoices': invoices,
            'tipo_documento':query_results.tipo_documento,
            'Cantidad_Docs_x_Tipo':query_results.Cantidad_Docs_x_Tipo,
            'afecto':query_results.afecto,
            'exento':query_results.exento,
            'Iva':query_results.Iva,
            'Total':query_results.Total,
        }
        
        #if table_query:
        #    raise UserError(f"valor de table_query => {table_query}")
        #else:
        #    raise UserError(f"valor de table_query => {table_query}")
      
        
        return report_values
