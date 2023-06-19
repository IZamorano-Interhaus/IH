# -*- coding: utf-8 -*-

from odoo import models, fields, api


class update_asiento(models.Model):
    _inherit = 'account.move'
    
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

