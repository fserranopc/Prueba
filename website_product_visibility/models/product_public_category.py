# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ProductPublicCategory(models.Model):
	_inherit = 'product.public.category'

	def get_child_categories(self):
		### Array
		all_category_ids = []
		for rec in self:
			all_category_ids.append(rec.id)
		### Si la categoria tiene hijos
			if rec.child_id:
				### Guardamos las categorias hijas
				categs = rec.child_id
				### Mientras que existan categorias
				while(categs):
					### Guardamos los ids de las categorias
					category_ids = rec.child_id.ids
					### Agregamos la información al array general
					all_category_ids.extend(category_ids)
					### Buscamos las categorias hijas
					categs = rec.search([('parent_id','in',category_ids)])
		return all_category_ids