# -*- coding: utf-8 -*-

from odoo import models, fields, api


class update_fields(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        selection_add=[("posted", "Contabilizado")]
    )
class purchaseorder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(
        selection_add=[("posted", "Contabilizado"),
                       ("cancel","Cancelado"),
                        ("locked","Bloqueado"),
                        ("purchase","Orden de compra"),
                        ("done","Terminado"),
                        ("cancel","Cancelado")]
    )