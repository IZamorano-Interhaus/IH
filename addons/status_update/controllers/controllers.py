# -*- coding: utf-8 -*-
# from odoo import http


# class StatusUpdate(http.Controller):
#     @http.route('/status_update/status_update', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/status_update/status_update/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('status_update.listing', {
#             'root': '/status_update/status_update',
#             'objects': http.request.env['status_update.status_update'].search([]),
#         })

#     @http.route('/status_update/status_update/objects/<model("status_update.status_update"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('status_update.object', {
#             'object': obj
#         })
