# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from itertools import groupby
from markupsafe import Markup
import re
from collections import defaultdict
from odoo import api, fields, models, SUPERUSER_ID, _, osv, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, format_amount, format_date, html_keep_url, is_html_empty
from odoo.tools.sql import create_index

from odoo.addons.payment import utils as payment_utils



FIGURE_TYPE_SELECTION_VALUES = [
    ('monetary', "Monetary"),
    ('percentage', "Percentage"),
    ('integer', "Integer"),
    ('float', "Float"),
    ('date', "Date"),
    ('datetime', "Datetime"),
    ('none', "No Formatting"),
]

DOMAIN_REGEX = re.compile(r'(-?sum)\((.*)\)')


class nuevo(models.Model):
    _inherit="sale.order"
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
        return report_values
        
class AccountReport(models.Model):
    _inherit ="account.report"
    
    _description = "Libro de Compras Report"
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
        return report_values
        
class AccountReportLine(models.Model):
    _inherit = "account.report.line"
    _description = "Accounting Report Line"
    _order = 'sequence, id'

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
        return report_values
        
class AccountReportExpression(models.Model):
    _inherit = "account.report.expression"
    _description = "Accounting Report Expression"
    _rec_name = 'report_line_name'

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
        return report_values
        
class AccountReportColumn(models.Model):
    _inherit = "account.report.column"
    _description = "Accounting Report Column"
    _order = 'sequence, id'

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
        return report_values