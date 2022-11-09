# -*- coding: utf-8 -*-
from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hide_var_list_view = fields.Boolean("Hide Variants List View",help="Hide product variants list view(multi-variants view for add to cart) on product page")

    def get_product_possible_variants(self):
        self.ensure_one()
        possible_variants = self.env["product.product"]
        for product in self.product_variant_ids:
            if self._is_combination_possible(combination=product.product_template_attribute_value_ids):
                possible_variants += product
        return possible_variants

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    # obtener el stock basado en la cantidad disponible de stock.quant
    def _get_available(self,id):
        # buscamos el producto, y la localizacion en este caso interna
        quant = self.env['stock.quant'].sudo().search([('product_id','=',id),('location_id.usage','=','internal')])
        # creamos un arreglo de la cantidad disponible de todos los registros y sumamos
        available = sum([q.available_quantity for q in quant])
        # devolvemos el stock
        return int(available)

    # buscar regla de abastecimiento para obtener el minimo (cantidades en tabla de variantes)
    def _get_min_qty(self,id):
        record = self.sudo().browse(id)
        rule = record.orderpoint_ids
        if rule:
            qty = rule[0].product_min_qty
        else:
            qty = 0
        return int(qty)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # buscar regla de abastecimiento para obtener el minimo (cantidades en tabla de variantes)
    def _get_min_qty(self,id):
        record = self.env['stock.warehouse.orderpoint'].sudo().search([('product_tmpl_id','=',id)])

        _logger.error("👽")
        _logger.error(record)
        _logger.error("👽")
        # rule = record.orderpoint_ids
        if record:
            qty = record[0].product_min_qty
        else:
            qty = 0
        return int(qty)