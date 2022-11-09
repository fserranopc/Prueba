# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	def _get_right_to_price(self):
		return self._get_right_to_sell('price')

	def _get_right_to_sell(self,type='sell'):
		self.ensure_one()
		response = False
		### Instanciamos objetos
		rights_obj = self.env['website.product.rights']
		### Buscamos el usuario que ejecutó el método
		user_id = self.env.user
		website_id = self._context.get('website_id') or 0
		if website_id !=1 or user_id._is_public():
			return True
		else:
			### buscamos si tiene permisos asignados
			right_ids = rights_obj.search([('rights','=',type)]).filtered(lambda x: user_id.id in x.user_ids.ids)
			### recorremos los permisos de compra
			for right_id in right_ids:
				### Si el permiso está basado en plantillas
				if right_id.type == 'template':
					### Si el producto se encuentra en la lista de productos
					if self.id in right_id.mapped('product_tmpl_ids').ids:
						if type == 'price':
							if right_id.rights == 'price':
								response = True
							else:
								response = False
						else:
							### validamos el tipo de permiso
							if right_id.rights == 'readonly':
								response = False
							else:
								### Enviamos un verdadero
								response = True 
				### Si el permiso esta basado en variantes
				if right_id.type == 'product':
					### Si la variante se encuentra en la lista de productos
					if self.id in right_id.mapped('product_ids.product_tmpl_id').ids:
						if type == 'price':
							if right_id.rights == 'price':
								response = True
							else:
								response = False
						else:
							### validamos el tipo de permiso
							if right_id.rights == 'readonly':
								response = False
							else:
								### Enviamos un verdadero
								response = True 
				### si el permiso esta basado en categoria
				if right_id.type == 'category':
					categ_ids = right_id.categ_ids.get_child_categories()
					for categ_id in categ_ids:
						if categ_id in self.public_categ_ids.ids:
							# si el tipo a buscar es precio
							if type == 'price':
								if right_id.rights == 'price':
									response = True
								else:
									response = False
							else:
								if right_id.rights == 'readonly':
									response = False
								else:
									response = True 
			return response