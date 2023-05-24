
const app = firebase.initializeApp(firebaseConfig);


function getFormData(formm) {
    var unindexed_array = formm.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}


function WriteTradeFirebase() {
    var trade_elements = document.getElementById("create-trade-form")
    var trade_elements_data = getFormData($(trade_elements))
    
    var entry_price = trade_elements_data['entry_price']
    var stop_loss = trade_elements_data['stop_loss']
    var target_price = trade_elements_data['target_price']
    var ticker_name = trade_elements_data['ticker_name']
    var ticker_symbol = trade_elements_data['symbol']

    var today_date = new Date();
    var today_date_str = today_date.getUTCFullYear() + "-" + today_date.getUTCMonth() + 1 + "-" + today_date.getUTCDate()

    firebase.database().ref('trades/' + today_date_str + "/" + ticker_symbol).set({
        EntryPrice: entry_price,
        TargetPrice: target_price,
        StopLoss: stop_loss,
        TickerName: ticker_name,
        TickerSymbol: ticker_symbol,
        TickerDate: today_date_str,
        TimeStamp: Date.now()
    })
}



document.getElementById("create-trade-form-submit").addEventListener("click", function () {
    WriteTradeFirebase()

})


