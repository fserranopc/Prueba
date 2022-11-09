odoo.define('website_variant_cart.change_qty_cart_lines', function (require) {
'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var wSaleUtils = require('website_sale.utils');
    require('website_sale.website_sale');
    var _t = core._t;
    
    // herencia al metodo original y remplazado
    publicWidget.registry.websiteSaleCart.include({
        /**
         * @private
         * @param {Event} ev
         */
        _onClickDeleteProduct: function (ev) {
            ev.preventDefault(); // original
            // cuando se seleccione eliminar se agrega una bandera en el tr actual 
            // para determinar que se puede bajar a 0 sin afectar el minimo establecido
            var is_delete = $(ev.target).closest('tr').find('input[name="is_delete"]')
            $(is_delete).val(1)
            // continua con lo que normalmente hace la funcion
            $(ev.currentTarget).closest('tr').find('.js_quantity').val(0).trigger('change');
        },
    })

    // herencia al metodo original y remplazado
    publicWidget.registry.WebsiteSale.include({
        /**
         * @private
         * Este metodo actualiza las cantidades y precios en el carrito de compra
         */
        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
            //creamos variables a consultar
            let apply_min = this._ValidateStock($input)
            let type = $($input).closest('tr').find('input[name="stock_type"]').val()
            var qty_min = parseInt($($input).closest('tr').find('.td-qty').find('#min_qty').text());
            var is_delete = parseInt($($input).closest('tr').find('input[name="is_delete"]').val())
            var moq = $($input).closest('tr').find('.moq')
            // si no tiene stock, vamos a configurarle una cantidad minima
            if (apply_min == 0 && type == 'product'){
                // cuando la cantidad actual sea menor al minimo, forzamos para que no pueda bajar
                if (value < qty_min){
                    // variable is_delete, solo verifica si es eliminacion (dado que baja a 0, ver funcion anterior)
                    // de ser el caso actualizamos el carrito sin forzar el minimo
                    if (is_delete == 1){
                        this._UpdateData($input, value, $dom_optional, line_id, productIDs) // funcion original, solo se mueve para reciclarla
                    }
                    // en caso contrario que la cantidad actual baje sobre el minimo, forzamos a no actualizar y mantener dicha cantidad
                    else{
                        $($input).val(qty_min)
                        $(moq).fadeIn('slow')
                    }
                }
                // en caso de que sea mayor, actualizamos de manera normal
                else{
                    this._UpdateData($input, value, $dom_optional, line_id, productIDs) // funcion original, solo se mueve para reciclarla
                }
            }
            // en caso de que tenga stock, actualizamos de manera normal
            else{
                this._UpdateData($input, value, $dom_optional, line_id, productIDs) // funcion original, solo se mueve para reciclarla
            }
        },
        /**
         * @private
         * Parte de la funcion original _changeCartQuantity
         * no se modifica nada, funcionamiento actual, busca los precios, actualiza el carrito y las vistas
         */
        _UpdateData: function($input, value, $dom_optional, line_id, productIDs){
                _.each($dom_optional, function (elem) {
                    $(elem).find('.js_quantity').text(value);
                    productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
                });
                $input.data('update_change', true);

                this._rpc({
                    route: "/shop/cart/update_json",
                    params: {
                        line_id: line_id,
                        product_id: parseInt($input.data('product-id'), 10),
                        set_qty: value
                    },
                }).then(function (data) {
                    $input.data('update_change', false);
                    var check_value = parseInt($input.val() || 0, 10);
                    if (isNaN(check_value)) {
                        check_value = 1;
                    }
                    if (value !== check_value) {
                        $input.trigger('change');
                        return;
                    }
                    if (!data.cart_quantity) {
                        return window.location = '/shop/cart';
                    }
                    wSaleUtils.updateCartNavBar(data);
                    $input.val(data.quantity);
                    $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);

                    if (data.warning) {
                        var cart_alert = $('.oe_cart').parent().find('#data_warning');
                        if (cart_alert.length === 0) {
                            $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                                    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                        }
                        else {
                            cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                        }
                        $input.val(data.quantity);
                    }
                });
        },
        /**
         * @private
         * Funcion que devuelve la cantidad de stock, disponible
         * 0 inicia el proceso de minimo
         * > 0 funciona de manera normal
         */
        _ValidateStock: function(td){
            let stock = $(td).closest('tr').find('.td-qty')
            let stock_qty = $(stock).find('#stock').text()
            return parseInt(stock_qty)
        }

    })

});