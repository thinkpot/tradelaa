(function () {
    if (getCookie('broker') != null) {
        $("#execute_trade_final").on("click", function () {
            var target_price = $("#modal_target_price_input").val();
            var stop_loss = $("#modal_stop_price_input").val();
            var entry_price = $("#modal_entry_price_input").val();
            var quantity = $("#quantity_param").val();
            var symbol =  $("#modal_trade_symbol").attr('aria-label');
            var side;
            if ($("#modal_side_input").val() == '2') {
                side = -1
            }
            else if ($("#modal_side_input").val() == '1') {
                side = 1
            }

            if (getCookie('broker') == 'fyers') {
                console.log("Sending trade to fyers")
                MainFyers.execute_trade_fyers(symbol, target_price, stop_loss, entry_price, quantity, side)
            }
        })

    }
})();


