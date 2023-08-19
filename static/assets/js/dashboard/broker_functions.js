function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


class BrokerFunction {
    constructor(broker, api_key, base_url) {
        this.broker = broker
        this.api_key = api_key
        this.base_url = base_url
    }

    execute_trade_fyers(symbol, target, stoploss, entry, quantity, side) {
        var response;
        $.ajax({
            type: "POST",
            url: this.base_url + "orders",
            data: {
                "symbol": "NSE:" + symbol,
                "qty": quantity,
                "type": 1,
                "side": side,
                "productType": "INTRADAY",
                "limitPrice": entry,
                "stopPrice": 0,
                "validity": "DAY",
                "disclosedQty": 0,
                "offlineOrder": "False",
                "stopLoss": stoploss,
                "takeProfit": target
            },
            headers: {
                "Authorizaiton": this.api_key + ":" + getCookie('access_token'),
            },
            xhrFields: {
                withCredentials: true
            },
            success: function (res) {
                console.log("Sending trade to Fyers")
                response = res;
            }
        })
        return response;
    }

    
}

let broker = getCookie('broker');
let MainFyers;
if (broker != null) {
    if (broker == 'fyers') {
        let main_api_key = 'NV1BMN088J-100';
        let base_url = 'https://api.fyers.in/api/v2/';
        MainFyers = new BrokerFunction('fyers', main_api_key, base_url)
    }
}