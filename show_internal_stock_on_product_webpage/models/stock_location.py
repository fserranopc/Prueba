# -*- coding: utf-8 -*-
from odoo import models, api, fields

class StockLocation(models.Model):
    _inherit = 'stock.location'

    stock_website = fields.Boolean(string='Stock disponible en sitio web',default=True)