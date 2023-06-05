# Fixed/Percentage discount on Purchase Order Lines
# Copyright (c) 2021 Sayed Hassan (sh-odoo@hotmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    x_studio_discount = fields.Float(string='% Disc.',compute="_onchange_discount", readonly = False, default=0.000)
    x_studio_fixed_discount = fields.Float(string="Fixed Disc.",compute="_onchange_fixed_discount", readonly = False, default=0.000)

    @api.onchange("x_studio_discount")
    def _onchange_discount(self):
        for line in self:
            if line.x_studio_discount !=0:
                self.x_studio_fixed_discount = 0.0
                x_studio_fixed_discount = (line.price_unit * line.product_qty) * (line.x_studio_discount / 100.0)
                
                precio_subtotal= line.price_subtotal - x_studio_fixed_discount
                
                line.update({"x_studio_fixed_discount": x_studio_fixed_discount,
                             "price_subtotal":precio_subtotal})
                
            if line.x_studio_discount == 0:
                x_studio_fixed_discount = 0.000
                line.update({"x_studio_fixed_discount": x_studio_fixed_discount})

    @api.onchange("x_studio_fixed_discount")
    def _onchange_fixed_discount(self):
        for line in self:
            if line.x_studio_fixed_discount != 0:
                line.x_studio_discount = 0.0
                x_studio_discount = ((line.product_qty * line.price_unit) - ((line.product_qty * line.price_unit) - line.x_studio_fixed_discount)) / (line.product_qty * line.price_unit) * 100 or 0.0
                line.update({"x_studio_discount": x_studio_discount})
            if line.x_studio_fixed_discount == 0:
                x_studio_discount = 0.0
                line.update({"x_studio_discount": x_studio_discount})
                  
            

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        price_unit_w_discount = self.price_unit
        for record in self:
            if record.x_studio_discount != 0:
                price_unit_w_discount = record.price_unit * (1 - (record.x_studio_discount / 100.0))
                precio_subtotal= record.price_subtotal - price_unit_w_discount  
        return {
            'price_subtotal' : precio_subtotal,
            'price_unit': price_unit_w_discount,
            'currency': self.order_id.currency_id,
            'quantity': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
        }
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    