# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class account_move(models.Model):
    _inherit="hr.expense.sheet"       

    
    afecto = fields.Monetary(string="Afecto", compute="_compute_amount",currency_field='currency_id',)

    exento = fields.Monetary(string="Exento", compute="_compute_amount",currency_field='currency_id',)
    
    @api.depends('expense_line_ids.total_amount_company', 'expense_line_ids.amount_tax_company')
    def _compute_amount(self):
        for sheet in self:
            sheet.total_amount = sum(sheet.expense_line_ids.mapped('total_amount_company'))
            sheet.total_amount_taxes = sum(sheet.expense_line_ids.mapped('amount_tax_company'))
            sheet.untaxed_amount = sheet.total_amount - sheet.total_amount_taxes

            sheet.afecto = sheet.total_amount_taxes/0.19
            sheet.exento = sheet.untaxed_amount-(sheet.total_amount_taxes/0.19)
    
