# -*- coding: utf-8 -*-

from odoo import models, fields, api


class status_update(models.Model):
    _inherit='account.move'


    state = fields.Selection([
       ('draft', 'Borradoras'),
        ('posted', 'Contabilizadas'),
        ('cancel', 'Por reingresar'),
        
    ], string='Estado', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')