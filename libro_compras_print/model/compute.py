# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class account_move(models.Model):
    _inherit="account.move.line"       

    afecto = fields.Float(string="afecto", compute="compute_afecto_exento")

    exento = fields.Float(string="exento", compute="compute_afecto_exento")
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def compute_afecto_exento(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']
            line.update({
                'afecto': amount_tax/0.19,
                'exento':amount_untaxed - (amount_tax/0.19),
            })