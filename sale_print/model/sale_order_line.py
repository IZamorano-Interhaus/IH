 # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    costo_directo= fields.Float(string="Costo Directo" , digits="Discount")
    gastos_generales = fields.Float(string="Gastos generales(%)", digits="Discount")
    utilidades = fields.Float(string="Utilidades(%)", digits="Discount")
    
    valor_gastos_generales = fields.Float(compute= "_compute_amount")
    valor_utilidades = fields.Float(compute = "_compute_amount")
    valor_costo_directo = fields.Float(compute= "_compute_amount")
    
    item = fields.Char(string="Item")  
    
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True, precompute=True)
    price_tax = fields.Float(
        string="Total Tax",
        compute='_compute_amount',
        store=True, precompute=True) 
    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Entry',
        required=True,
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
        check_company=True,
    )
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
            
            line.valor_costo_directo = line.product_uom_qty * line.price_unit
            line.valor_gastos_generales = (line.gastos_generales / 100) * line.valor_costo_directo
            line.valor_utilidades = (line.utilidades / 100) * line.valor_costo_directo

            
            line.update({
                'valor_costo_directo':  line.product_uom_qty * line.price_unit,
                'valor_gastos_generales':(line.gastos_generales / 100) * self.valor_costo_directo,
                'valor_utilidades':amount_untaxed * self.utilidades,
                'price_tax':amount_tax,
                'price_subtotal':self.valor_costo_directo + self.gastos_generales + self.utilidades,
            })
    @api.depends('product_uom_qty','discount','price_unit','tax_id')
    def _compute_subtotal(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_tax = totals['amount_tax']
            amount_untaxed = line.product_uom_qty * (line.price_unit - (line.price_unit * line.discount / 100))
            line.update(
                {
                    'price_tax':amount_tax,
                    'price_subtotal':self.valor_costo_directo + self.valor_gastos_generales + self.valor_utilidades,
                    'price_total': self.price_subtotal + amount_tax,
                }
            )