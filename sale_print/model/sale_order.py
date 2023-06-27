# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    costo_directo= fields.Float()

    gastos_generales = fields.Float()

    utilidades = fields.Float()

    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    