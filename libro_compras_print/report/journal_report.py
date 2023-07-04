# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

from odoo.addons.account.models.account_move import PAYMENT_STATE_SELECTION

from functools import lru_cache


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

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
        return '%s %s %s' % (self.query_select(), self.query_from())

    @api.model
    def query_select(self):
        return '''
            select to_char(move.invoice_date_due , 'TMMonth') as mes, 
            doc.code||' - '||doc.name tipo_documento,
            move.name numero,
            move.invoice_date_due fecha,
            move.ref nombre,
            move.amount_untaxed importe_libre_impuesto,
            move.amount_tax impuesto,
            move.amount_total total
            
        '''

    @api.model
    def query_from(self):
        return '''
            from account_move move
            inner join l10n_latam_document_type doc
            	on move.l10n_latam_document_type_id = doc.id
            order by move.invoice_date_due desc
        '''

    