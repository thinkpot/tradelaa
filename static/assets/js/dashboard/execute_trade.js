(function () {
    if (getCookie('broker') != null) {
        $("#execute_trade_final").on("click", function () {
            var target_price = $("#modal_target_price_input").val();
            var stop_loss = $("#modal_stop_price_input").val();
            var entry_price = $("#modal_entry_price_input").val();
            var quantity = $("#quantity_param").val();
            var symbol = $("#modal_trade_symbol").attr('aria-label');
            var side;
            if ($("#modal_side_input").val() == '2') {
                side = -1
            }
            else if ($("#modal_side_input").val() == '1') {
                side = 1
            }

            var payload = {
                "symbol": "NSE:"+symbol+"-EQ",
                "qty": quantity,
                "type": 1,
                "side": side,
                "productType": "INTRADAY",
                "limitPrice": entry_price,
                "stopPrice": 0,
                "validity": "DAY",
                "disclosedQty": 0,
                "offlineOrder": "False",
                "takeProfit": target_price,
                "stopLoss": stop_loss,
            }

            if (getCookie('broker') == 'fyers') {
                console.log("Executing trade")
                fetch("/dashboard/execute-fyers-trade/", {
                    body:JSON.stringify(payload),
                    method:"POST",
                    headers:{
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    console.log("daata ", data)
                })
            }
        })

    }
})();


