# -*- coding: utf-8 -*-
{
    "name" : "Website Product Visibility Odoo",
    "version" : "13.0.1.3",
    "description": """
        Permite asignar permisos para la visualización de productos en el sitio web
    """,
    "category" : "eCommerce",
    "depends" : [
        'base',
        'sale_management',
        'website',
        'website_sale',
        'website_variant_cart',
        'portal',
        'mail'],
    "author": "Pegasus Control",
    'summary': 'coded by: Eduardo Serrano (fserranopc@corporativosade.com.mx)',
    "website" : "https://pegasus.com.mx",
    'qweb': [
        'static/src/xml/searchbar.xml',
        'static/src/xml/recently_viewed.xml'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/website_product_rights_view.xml',
        #'views/product_visibility_template.xml',
        'views/price_visibility_template.xml',
    ],
    'qweb': [],
    "auto_install": False,
    'assets' : {
        'web.assets_frontend': [
            '/website_product_visibility/static/src/js/load_template.js',
            '/website_product_visibility/static/src/js/searchbar.js',
        ]
    },
    "installable": True,
}
