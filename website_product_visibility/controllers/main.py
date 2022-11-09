# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
#from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    # --------------------------------------------------------------------------
    # Products Search Bar
    # --------------------------------------------------------------------------

    @http.route('/shop/products/autocomplete', type='json', auth='public', website=True)
    def products_autocomplete(self, term, options={}, **kwargs):
        # self = Website
        """
        Returns list of products according to the term and product options

        Params:
            term (str): search term written by the user
            options (dict)
                - 'limit' (int), default to 5: number of products to consider
                - 'display_description' (bool), default to True
                - 'display_price' (bool), default to True
                - 'order' (str)
                - 'max_nb_chars' (int): max number of characters for the
                                        description if returned

        Returns:
            dict (or False if no result)
                - 'products' (list): products (only their needed field values)
                        note: the prices will be strings properly formatted and
                        already containing the currency
                - 'products_count' (int): the number of products in the database
                        that matched the search query
        """
        ProductTemplate = request.env['product.template']

        display_description = options.get('display_description', True)
        display_price = options.get('display_price', True)
        order = self._get_search_order(options)
        max_nb_chars = options.get('max_nb_chars', 999)

        category = options.get('category')
        attrib_values = options.get('attrib_values')

        domain = self._get_search_domain(term, category, attrib_values, display_description)
        products = ProductTemplate.search(
            domain,
            limit=min(20, options.get('limit', 5)),
            order=order
        )
        # Override in this line, add the field 'website_allow_to_sell'
        fields = ['id', 'name', 'website_url', 'website_allow_to_sell']
        if display_description:
            fields.append('description_sale')

        res = {
            'products': products.read(fields),
            'products_count': ProductTemplate.search_count(domain),
        }

        if display_description:
            for res_product in res['products']:
                desc = res_product['description_sale']
                if desc and len(desc) > max_nb_chars:
                    res_product['description_sale'] = "%s..." % desc[:(max_nb_chars - 3)]

        if display_price:
            FieldMonetary = request.env['ir.qweb.field.monetary']
            monetary_options = {
                'display_currency': request.website.get_current_pricelist().currency_id,
            }
            for res_product, product in zip(res['products'], products):
                combination_info = product._get_combination_info(only_template=True)
                res_product.update(combination_info)
                res_product['list_price'] = FieldMonetary.value_to_html(res_product['list_price'], monetary_options)
                res_product['price'] = FieldMonetary.value_to_html(res_product['price'], monetary_options)

        return res

    # --------------------------------------------------------------------------
    # Products Recently Viewed
    # --------------------------------------------------------------------------
    @http.route('/shop/products/recently_viewed', type='json', auth='public', website=True)
    def products_recently_viewed(self, **kwargs):
        return self._get_products_recently_viewed()

    def _get_products_recently_viewed(self):
        """
        Returns list of recently viewed products according to current user
        """
        max_number_of_product_for_carousel = 12
        visitor = request.env['website.visitor']._get_visitor_from_request()
        if visitor:
            excluded_products = request.website.sale_get_order().mapped('order_line.product_id.id')
            products = request.env['website.track'].sudo().read_group(
                [('visitor_id', '=', visitor.id), ('product_id', '!=', False), ('product_id.website_published', '=', True), ('product_id', 'not in', excluded_products)],
                ['product_id', 'visit_datetime:max'], ['product_id'], limit=max_number_of_product_for_carousel, orderby='visit_datetime DESC')
            products_ids = [product['product_id'][0] for product in products]
            if products_ids:
                viewed_products = request.env['product.product'].with_context(display_default_code=False).browse(products_ids)

                FieldMonetary = request.env['ir.qweb.field.monetary']
                monetary_options = {
                    'display_currency': request.website.get_current_pricelist().currency_id,
                }
                rating = request.website.viewref('website_sale.product_comment').active
                res = {'products': []}
                for product in viewed_products:
                    combination_info = product._get_combination_info_variant()
                    # Override in this line, add the field 'website_allow_to_sell'
                    res_product = product.read(['id', 'name', 'website_url', 'website_allow_to_sell'])[0]
                    res_product.update(combination_info)
                    res_product['price'] = FieldMonetary.value_to_html(res_product['price'], monetary_options)
                    if rating:
                        res_product['rating'] = request.env["ir.ui.view"].render_template('website_rating.rating_widget_stars_static', values={
                            'rating_avg': product.rating_avg,
                            'rating_count': product.rating_count,
                        })
                    res['products'].append(res_product)
                return res
        return {}