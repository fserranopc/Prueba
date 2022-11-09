# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class WebsiteProductRights(models.Model):
    _inherit = 'website.product.rights'

    # new fields to control the dashboard
    dashboard_all = fields.Boolean(string='Seleccionar todo')
    dashboard_quote = fields.Boolean(string='Cotizaciones')
    dashboard_order = fields.Boolean(string='Órdenes de venta')
    dashboard_invoice = fields.Boolean(string='Facturas')
    dashboard_timesheet = fields.Boolean(string='Hojas de horas')
    dashboard_project = fields.Boolean(string='Proyectos')
    dashboard_tasks = fields.Boolean(string='Tareas')
    dashboard_purchase = fields.Boolean(string='Pedidos de compra')
    dashboard_account = fields.Boolean(string='Información')
    dashboard_ticket = fields.Boolean(string='Tickets')
    dashboard_rfq = fields.Boolean(string='Solicitudes de cotización')
    dashboard_subscription = fields.Boolean(string='Suscripciones')

    # select/deselect all
    @api.onchange('dashboard_all')
    def select_all_dashboard(self):
        if self.dashboard_all:
            self._add_remove_dashboard(True)
        else:
            self._add_remove_dashboard(False)

    def _add_remove_dashboard(self,value):
        self.dashboard_quote = value
        self.dashboard_order = value
        self.dashboard_invoice = value
        self.dashboard_timesheet = value
        self.dashboard_project = value
        self.dashboard_tasks = value
        self.dashboard_purchase = value
        self.dashboard_account = value
        self.dashboard_ticket = value
        self.dashboard_rfq = value
        self.dashboard_subscription = value