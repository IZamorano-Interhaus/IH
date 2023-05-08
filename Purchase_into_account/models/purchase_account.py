# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class reporte_detalle(models.Model):
    _inherit=['purchase.order.line','account.move.line']

class OrdenCompra(models.Model):
    _inherit=['purchase.order','account.move']
    
    
    
    

