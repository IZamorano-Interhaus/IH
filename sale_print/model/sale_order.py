# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    costo_directo= fields.Monetary(string="Costo directo", compute = "_compute_amount")

    gastos_generales = fields.Float(string="Gastos generales(%)", digits="Discount")
    valor_gastos_generales = fields.Float(compute= "_compute_amount")
    utilidades = fields.Float(string="Utilidades(%)", digits="Discount")
    valor_utilidades = fields.Float(compute = "_compute_amount")
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True, precompute=True)
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']

            line.update({
                'costo_directo': amount_untaxed,
                'valor_gastos_generales':amount_untaxed * self.gastos_generales,
                'valor_utilidades':amount_untaxed * self.utilidades,
                'price_tax': amount_tax,
                
            })
    def _compute_subtotal(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_tax = totals['amount_tax']
            line.update(
                {
                    'price_subtotal':self.costo_directo+self.valor_gastos_generales+self.valor_utilidades,
                    'price_total': self.price_subtotal + amount_tax,
                }
            )

