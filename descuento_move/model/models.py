# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    descuento = fields.Monetary(
        string='Descuento ($)',
        compute='_compute_descuento',
        store=True,
        readonly=False,
        digits='Product Price'
    )
    discount = fields.Monetary(
        string='Discount (%)',
        compute='_compute_discount',
        store=True,
        digits=(12,3)
    )

    @api.depends('descuento')
    def _compute_discount(self):
        
        for line in self:
            if line.price_subtotal != 0:
                line.discount = round(line.descuento * 100 / (line.price_unit * line.quantity),10)
            else:
                line.discount = 0

    @api.depends('price_unit', 'discount')
    def _compute_descuento(self):
        for line in self:
            line.descuento = line.price_unit * line.discount
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'posted':  # Ajusta aquí el estado deseado ('posted', 'contabilizado', etc.)
            self.descuento.readonly = False
        else:
            self.descuento.readonly = True
    def write(self, values):
        if 'descuento' in values:
            if self.price_subtotal != 0:
                values['discount'] = values['descuento'] * 100 / self.price_subtotal
            else:
                values['discount'] = 0
        return super(AccountMoveLine, self).write(values)

    def _prepare_analytic_distribution_line(self, distribution, account_id, distribution_on_each_plan):
        """ Prepare the values used to create() an account.analytic.line upon validation of an account.move.line having
            analytic tags with analytic distribution.
        """
        self.ensure_one()
        account_id = int(account_id)
        account = self.env['account.analytic.account'].browse(account_id)
        distribution_plan = distribution_on_each_plan.get(account.root_plan_id, 0) + distribution
        decimal_precision = self.env['decimal.precision'].precision_get('Percentage Analytic')
        if float_compare(distribution_plan, 100, precision_digits=decimal_precision) == 0:
            amount = -self.balance * (100 - distribution_on_each_plan.get(account.root_plan_id, 0)) / 100.0
        else:
            amount = -self.balance * distribution / 100.0
        distribution_on_each_plan[account.root_plan_id] = distribution_plan
        default_name = self.name or (self.ref or '/' + ' -- ' + (self.partner_id and self.partner_id.name or '/'))
        return {
            'name': default_name,
            'date': self.date,
            'account_id': account_id,
            'partner_id': self.partner_id.id,
            'unit_amount': self.quantity,
            'product_id': self.product_id and self.product_id.id or False,
            'product_uom_id': self.product_uom_id and self.product_uom_id.id or False,
            'amount': amount,
            'general_account_id': self.account_id.id,
            'ref': self.ref,
            'move_line_id': self.id,
            'user_id': self.move_id.invoice_user_id.id or self._uid,
            'company_id': account.company_id.id or self.company_id.id or self.env.company.id,
            'category': 'invoice' if self.move_id.is_sale_document() else 'vendor_bill' if self.move_id.is_purchase_document() else 'other',
        }