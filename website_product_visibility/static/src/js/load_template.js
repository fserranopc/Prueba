odoo.define('website_product_visibility.load_template', function (require) {
'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;

    ajax.loadXML('/website_product_visibility/static/src/xml/searchbar.xml', qweb);
    ajax.loadXML('/website_product_visibility/static/src/xml/recently_viewed.xml', qweb);

});