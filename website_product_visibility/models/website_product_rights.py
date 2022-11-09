# -*- coding: utf-8 -*-
from odoo import api, models, fields

PIVOT_OPTIONS = [
    ('template','Plantilla de Producto'),
    ('product','Variante de Producto'),
    ('category','Categoría')]

RIGHTS_OPTIONS = [
    ('readonly','Visualización'),
    ('sell','Comprar'),
    ('price','Precio')]

class WebsiteProductRights(models.Model):
    _name = 'website.product.rights'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'sequence.mixin']
    _description = 'Tabla de permisos para productos en website'

    name = fields.Char(string='Nombre del permiso',
        tracking=True,
        required=True)

    type = fields.Selection(selection=PIVOT_OPTIONS, 
        string='Aplicación de permiso',
        tracking=True,
        default='template',
        required=True)

    website_id = fields.Many2one(comodel_name='website',
        string='Sitio web',
        tracking=True,
        required=True)

    rights = fields.Selection(selection=RIGHTS_OPTIONS,
        string='Permisos de',
        tracking=True,
        default='readonly')

    date = fields.Date(string='Date',
        copy=False,
        default=fields.Date.context_today,
        index=True)

    user_ids = fields.Many2many(comodel_name='res.users',
        string='Usuarios')

    product_tmpl_ids = fields.Many2many(comodel_name='product.template',
        column1="right_id",
        column2="product_tmpl_id",
        relation="product_tmpl_rights_website",
        string='Plantilla de productos')

    product_ids = fields.Many2many(comodel_name='product.product',
        column1="right_id",
        column2="product_id",
        relation="product_rights_website",
        string='Variante de productos')

    categ_ids = fields.Many2many(comodel_name='product.public.category',
        column1="right_id",
        column2="public_categ_id",
        relation="category_rights_website",
        string='Categorías de productos')

    @api.onchange('type')
    def onchange_type(self):
        ### limpiamos las demás categorias
        if self.type == 'product':
            self.product_tmpl_ids = [(5, 0, 0)]
            self.categ_ids = [(5, 0, 0)]
        elif self.type == 'template':
            self.product_ids = [(5, 0, 0)]
            self.categ_ids = [(5, 0, 0)]
        elif self.type == 'categ_ids':
            self.product_ids = [(5, 0, 0)]
            self.product_tmpl_ids = [(5, 0, 0)]
