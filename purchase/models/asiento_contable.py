# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from markupsafe import escape, Markup
from pytz import timezone, UTC
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_amount, format_date, formatLang, get_lang, groupby
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError, ValidationError


class AsientoContable(models.Model):
    _name = "asiento.contable"
    _inherit = ['purchase.order', 'purchase.order.line', 'account.move.line']
    _description = "Asiento contable"
    _rec_names_search = ['name', 'partner_ref']
    _order = 'priority desc, id desc'

    def draft_asiento(self):
        data_OC = {
                'ref':None,
                'partner_id':None,
            }
        """ 
        for move in self:
            if any(
                move.env['account.account_move.ref']!=order.name
            ):
                self.write({
                    
                    'ref':order.name,
                    'partner_id':order.partner_id,
                    'analytic_distribution':order.x_studio_many2one_field_x10XM,
                    'account_id':order.x_studio_cuenta_contable,
                }) 
            """
        return data_OC