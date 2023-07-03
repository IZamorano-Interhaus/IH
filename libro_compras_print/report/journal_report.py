# -*- coding: utf-8 -*-

# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class SaleOrderLine(models.Model):
    _inherit="sale.order.line"
    #l10n_cl.view_complete_invoice_refund_tree