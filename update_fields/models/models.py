# -*- coding: utf-8 -*-

from odoo import models, fields, api


class update_fields(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        selection_add=[("posted", "Contabilizado")]
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente/Proveedor',
        readonly=True,
        tracking=True,
        states={'draft': [('readonly', False)]},
        check_company=True,
        change_default=True,
        ondelete='restrict',
    )
class purchaseorder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(
        selection_add=[("posted", "Contabilizado"),("cancel","Cancelado")]
    )