# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class purchase_order(models.Model):
    _inherit="purchase.order"       

    afecto = fields.Monetary(string="Afecto", compute="_compute_amount")

    exento = fields.Monetary(string="Exento", compute="_compute_amount")
    
    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']
            line.update({
                'price_subtotal': self.amount_untaxed,
                'price_tax': self.amount_tax,
                'price_total': amount_untaxed + amount_tax,
                'afecto' : (self.amount_tax/0.19),
                'exento' : (self.amount_untaxed-(self.amount_tax/0.19)),
            })
    def _convert_to_tax_base_line_dict(self):
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.order_id.currency_id,
            product=self.product_id,
            taxes=self.taxes_id,
            price_unit=self.price_unit,
            quantity=self.product_qty,
            price_subtotal=self.price_subtotal,
        )
            
    