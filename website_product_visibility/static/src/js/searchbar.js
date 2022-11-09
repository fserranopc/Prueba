odoo.define('website_sale_hide_price.searchbar', function (require) {
    'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;

    // find attribute 
    var show_price = $("div").find("[name='t-att-data-display-price'] span").html()

    // if this price is False, load ajax and hide prices
    if (!show_price){
        ajax.loadXML('/website_sale_hide_price/static/src/xml/searchbar.xml', qweb);
    }


});