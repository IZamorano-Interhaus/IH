# -*- coding: utf-8 -*-

from odoo import models, fields, api


class update_fields(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        selection_add=[("posted", "Contabilizado")]
    )
