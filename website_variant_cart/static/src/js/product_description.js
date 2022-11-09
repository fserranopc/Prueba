odoo.define('website_variant_cart.website_product_variant_description', function(require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    
    var ajax = require('web.ajax');
    $(document).ready(function() {

        $(".var-show-description").click(function(){
            var button = $(this).closest('tr').next('tr')
            if (!$(this).hasClass("blank")){
                if ($(button).is(':visible')) {
                    $(button).fadeOut("slow");
                } else {
                    $(button).fadeIn("slow");
                }
            }
        });

        $('div.js_product.js_main_product',).on('change', function() {
            
            show_hide_stock_change();
        });

        function show_hide_stock_change() {
                var $form_data = $('div.js_product.js_main_product');
                var $js_qty = $form_data.find('.css_quantity.input-group.oe_website_spinner');
                var product_id = false
                if ($("input[name='product_id']").is(':radio')){
                    product_id = $form_data.find("input[name='product_id']:checked").val();
                } else {
                    var product_id = $form_data.find("input[name='product_id']").val();
                
                    var $description_data = $("#bi_variant_description.ayaz");
                    var $tab_data = $form_data.find('#tab1primary');
                    var $shubh_data = $description_data.find('.shubh');
                                    
                    var line_id= [];
                    var product;

                        for(var i=0; i < $shubh_data.length; i++){
                            line_id.push($shubh_data[i]['id'])

                        for(var j=0; j < line_id.length; j++){
                            product = line_id[j];
                    
                            if (product_id == product) {
                                if ($shubh_data[i]['id'] == product){
                                    $shubh_data[i].style.display="block";
                                }
                                else{
                                    $shubh_data[i].style.display="none";
                                }
                            } else {
                                $shubh_data[i].style.display="none";
                            }
                        }
                           }
                    }
                 }
        });
});;   
