# -*- coding: utf-8 -*-
{
  "name"                 :  "Website Multi Variant Add to Cart",
  "summary"              :  """This module allows customer to add multiple product variants with different quantities in cart at once.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Multi-Variant-Add-to-Cart.html",
  "description"          :  """https://webkul.com/blog/odoo-website-multi-variant-add-to-cart/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_variant_cart",
  "depends"              :  ['website_sale','show_internal_stock_on_product_webpage'],
  # por temas de errores
  "data"                 :  [
                             'views/multi_variant_template.xml',
                             'views/product_template_view.xml',
                             'views/product_description.xml',
                             'views/product_single_min.xml'
                            ],
  'assets'               : {
                          'web.assets_frontend': [
                              'website_variant_cart/static/**/*'
                          ],
  },
  "demo"                 :  [],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "USD",
}
