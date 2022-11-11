# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # obtener el stock basado en la cantidad disponible de stock.quant
    def _get_available_stock(self,id):
        # buscamos el producto, y la localizacion en este caso interna
        quant = self.env['stock.quant'].sudo().search([
            ('product_tmpl_id','=',id),
            ('location_id.usage','=','internal'),
            ('location_id.stock_website','=',True) # opcion para ignorar ciertas ubicaciones
        ])
        # creamos un arreglo de la cantidad disponible de todos los registros y sumamos
        available = sum([q.available_quantity for q in quant])
        # devolvemos el stock
        return int(available)