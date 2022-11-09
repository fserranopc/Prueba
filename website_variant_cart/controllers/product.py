# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools.translate import html_translate

class ProductProduct(models.Model):
    _inherit = "product.product"

    variant_description = fields.Html('Description for the Variant of the Product', sanitize_attributes=False, translate=html_translate)