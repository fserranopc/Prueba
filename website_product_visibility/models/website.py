# -*- coding: utf-8 -*-
from odoo import api, models, fields,SUPERUSER_ID, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.http import request


class Website(models.Model):
	_inherit = 'website'

	def sale_product_domain(self):
		### Validamos el sitio web
		if self._context.get('website_id') != 1:
			return super(Website, self).sale_product_domain()
		### Lista de plantilla de productos
		product_template_ids = []
		category_ids = []
		domain = []
		is_public = self.env.user._is_public()
		### Si es usuario publico del sistema
		if is_public:
			### Retornamos el método nativo
			return super(Website, self).sale_product_domain()
		### Si no
		else:
			### Nos instanciamos en el cliente
			user_id = self.env.user
			### buscamos todos los registros donde pertenece el usuario
			right_ids = request.env['website.product.rights'].search([]).filtered(lambda x: user_id.id in x.user_ids.ids)
			### recorremos los registros
			for right_id in right_ids:
				### Si la aplicación de permiso es plantilla
				if right_id.type == 'template':
					### Agregamos el producto a la lista
					product_template_ids.extend(right_id.product_tmpl_ids.ids)
				### Si la aplicación de permiso es de variante
				elif right_id.type == 'product':
					### Agregamos el producto a la lista
					product_template_ids.extend(right_id.product_ids.mapped('product_tmpl_id').ids)
				### Si la aplicación de permiso es de categoría
				elif right_id.type == 'category':
					### Agregamos la categoría a la lista de categorias
					category_ids.extend(right_id.categ_ids.get_child_categories())
			### Si tiene algún dato en la lista de productos
			if product_template_ids:
				### Lo agregamos al dominio
				domain.extend([('id', 'in', product_template_ids)])
			### Si tiene algún dato la lista de categorías
			if category_ids:
				### Lo agregamos al dominio
				domain.extend([('public_categ_ids','in',category_ids)])
			if not domain:
				domain.extend([('id','=',0)])
			if len(domain) > 1:
				### Retornamos el método nativo + los ids encontrados
				return ['&'] + super(Website, self).sale_product_domain() + ['|'] + domain
			else:
				return ['&'] + super(Website, self).sale_product_domain() + domain		

