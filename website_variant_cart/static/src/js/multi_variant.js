
odoo.define('website_variant_cart.multi_variant', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var utils = require('web.utils');
    var _t = core._t;

    $(document).ready(function() {

        // cuando se cumpla la condicion, poner en 0 la cantidad (productos individuales)
        var is_single_init = $('.p_variants').length
        var input_add_init =  $('input[type="text"][name="add_qty"]')
        var apply_min_init = parseInt($('#apply_min').text())
        var type_init = $('input[name="stock_type"]').val()
        if (is_single_init == 0 && apply_min_init == 0 && type_init == 'product'){
            input_add_init.val(0)
         }
        // cuando se cumpla la condicion, poner en 0 la cantidad (productos individuales)

        function str_to_price(str_price) {
            var l10n = _t.database.parameters;
            str_price = str_price.replace(l10n.thousands_sep, '');
            str_price = str_price.replace(l10n.decimal_point, '.');
            return parseFloat(str_price)
        }

        function price_to_str(price) {
            var l10n = _t.database.parameters;
            var precision = 2;
            if ($(".decimal_precision").length) {
                precision = parseInt($(".decimal_precision").last().data('precision'));
                if (!precision) { precision = 0; } //todo: remove me in master/saas-17
            }
            var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
            formatted[0] = utils.insert_thousand_seps(formatted[0]);
            return formatted.join(l10n.decimal_point);
        }

        function update_total_price(){
            var total = 0.0;
            var $form = $('.p_variants').closest("form");
            var $total_price = $form.find('#var-total-price');
            $('.p_variants').each(function(){
                var $subtotal = $(this).find('#var-subtotal');
                var subtotal = str_to_price($subtotal.find('.oe_currency_value').html());
                total = total + subtotal;
            });
            $total_price.find('.oe_currency_value').html(price_to_str(total));
        }

        function getCustomVariantValues(container) {
          var variantCustomValues = [];
          container.find('.p_variants_cust_val').each(function (){
              var $variantCustomValueInput = $(this);
              if ($variantCustomValueInput.length !== 0){
                  variantCustomValues.push({
                      'custom_product_template_attribute_value_id': $variantCustomValueInput.data('attribute_value_id'),
                      'attribute_value_name': $variantCustomValueInput.data('attribute_value_name'),
                      'custom_value': $variantCustomValueInput.val(),
                  });
              }
          });
          return variantCustomValues;
        }
        // minimo para productos individuales
        $('.js_product').find('input[type="text"][name="add_qty"]').on('change', function(ev){
            var is_single = $('.p_variants').length
            if (is_single == 0){
                let apply_min = parseInt($('#apply_min').text())
                let type = $('input[name="stock_type"]').val()
                var flag = $('input[name="stock_flag"]')
                var qty_min = parseInt($('#min_qty').text())
                var $this = $('input[type="text"][name="add_qty"]')
                var qty = parseInt($(this).val(),10);
                var moq = $('.moq')
                if (apply_min == 0 && type == 'product'){
                // si la cantidad minima es diferente de 0
                    if (qty_min != 0){
                        // usamos una bandera para verificar si ya aplicamos el minimo (para disminuir la cantidad)
                        if (flag.val() == 0){
                            // si la bandera es 0, ponemos el minimo y actualizamos el valor a 1
                            $($this).val(qty_min)
                            $(flag).val(1)
                            $(moq).fadeIn('slow')
                        }
                        // cuando la bandera sea 1, actualizara de manera normal la cantidad (partimiendo del minimo anterior)
                        else{
                            // si la cantidad es menor la minima, reseteamos a 0
                            if (qty == qty_min){
                                $(flag).val(1)
                            }
                            else if (qty < qty_min){
                                $(flag).val(0)
                                $($this).val(0)
                                $(moq).fadeOut()
                            }
                        }
                    }
                    // si no tiene configurado una cantidad minima, no actualizamos el campo
                    else{
                        $($this).val(0)
                    }
                }
            }
        });
        $('.p_variants').find('input[type="text"][name="add_qty"]').on('change', function(ev)
        {
            var $this = this
            let apply_min = validate_stock(this)
            let type = $(this).closest('tr').find('input[name="stock_type"]').val()
            var qty = parseInt($(this).val(),10);
            // var qty_input = $(this).closest('tr').find('input[name="add_qty"]').val()
            var qty_min = parseInt($(this).closest('tr').find('.stock_qty').find('p').text());
            var flag = parseInt($(this).closest('tr').find('input[name="stock_flag"]').val())
            var $flag = $(this).closest('tr').find('input[name="stock_flag"]')
            var moq = $(this).closest('tr').find('.moq')
            // vemos si no cuenta con stock
            if (apply_min == 0 && type == 'product'){
                // si la cantidad minima es diferente de 0
                if (qty_min != 0){
                    // usamos una bandera para verificar si ya aplicamos el minimo (para disminuir la cantidad)
                    if (flag == 0){
                        // si la bandera es 0, ponemos el minimo y actualizamos el valor a 1
                        $($this).val(qty_min)
                        $($flag).val(1)
                        $(moq).fadeIn('slow')
                    }
                    // cuando la bandera sea 1, actualizara de manera normal la cantidad (partimiendo del minimo anterior)
                    else{
                        // si la cantidad es menor la minima, reseteamos a 0
                        if (qty <= qty_min){
                            $($flag).val(0)
                            $($this).val(0)
                            $(moq).fadeOut()
                        }
                    }
                }
                // si no tiene configurado una cantidad minima, no actualizamos el campo
                else{
                    $($this).val(0)
                }
            }
            var add_qty = parseInt($(this).val(),10);
            var $p_variants = $(this).closest('.p_variants');
            var $subtotal = $p_variants.find('#var-subtotal');
            var $var_price = $p_variants.find('#var-price');
            var product_id = parseInt($p_variants.find('input[type="hidden"][name="product_id"]').first().val(),10);
            if(add_qty > 0){
                if ($var_price.length != 0){
                    ajax.jsonRpc("/vc/shop/get_unit_price", 'call', {'product_ids': product_id,'add_qty': add_qty})
                    .then(function (data) {
                        var value = data[product_id];
                        $var_price.find('.oe_currency_value').html(price_to_str(value));
                        $subtotal.find('.oe_currency_value').html(price_to_str(value*add_qty));
                        update_total_price();
                    });
                }
            }
            else{
                if ($var_price.length != 0){
                    $subtotal.find('.oe_currency_value').html(price_to_str(0));
                    update_total_price();
                }
            }
            // }
        });

        function validate_stock(td){
            let stock = $(td).closest('tr').find('.stock_qty')
            let stock_qty = $(stock).find('span').text()
            return parseInt(stock_qty)
        }

        var publicWidget = require('web.public.widget');
        require('website_sale.website_sale');

        publicWidget.registry.WebsiteSale.include({
            _onClickAdd: function(ev){
                ev.preventDefault();
                var variant_list_status = $('#variants_list_view_status').data('variant_list_status');
                if(!variant_list_status){
                    // en el caso que no apliquen variantes llamamos a la opcion de agregar de brittania
                    // retorna proceso normal si este no esta activo, es decir si solo es un producto
                    this._AddCartBrittania(ev)
                }
                var data = [];
                if (!$(ev.currentTarget).is(".disabled")) {
                    var variant_element = document.getElementById('p_variants');
                    if (variant_element != null) {
                        $('.p_variants').each(function(ev){
                            var dict = {};
                            var $this = $(this);
                            var product_id = parseInt($this.find('input[type="hidden"][name="product_id"]').first().val(),10);
                            var add_qty = parseInt($this.find('input[name="add_qty"]').first().val(),10);
                            var custom_value = getCustomVariantValues($this)
                            if(!isNaN(add_qty) && add_qty > 0){
                                dict["product_id"] = product_id;
                                dict["add_qty"] = add_qty;
                                dict['product_custom_attribute_values']= JSON.stringify(custom_value);
                                data.push(dict);
                            }
                        });
                        if(data.length == 0){
                            $('#multi-variant-error').show();
                            setTimeout(function() {
                                $('#multi-variant-error').hide();
                            },3000);
                        }
                        else{
                            ajax.jsonRpc("/shop/cart/update/multi/variant", 'call',
                            {
                                'data': data,
                            })
                            .then(function (result)
                            {
                                window.location.href = window.location.origin + result['redirect_url']
                                $(window).on('load',function() {});
                            });
                        }
                    }
                }
            }

        });

    });
});
