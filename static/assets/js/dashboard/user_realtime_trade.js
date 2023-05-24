
const app = firebase.initializeApp(firebaseConfig);

let entry_price, target_price, ticker_name, stop_loss, target, symbol;
var today_date = new Date();
var today_date_str = today_date.getUTCFullYear() + "-" + today_date.getUTCMonth() + 1 + "-" + today_date.getUTCDate()

let trades_main_wrapper = $("#trades_main_wrapper")

var entry = firebase.database().ref('trades/' + today_date_str)
entry.orderByChild('TimeStamp').startAt(Date.now()).on('child_added', (snapshot) => {
    let max_pl;
    entry_price = snapshot.val().EntryPrice
    target_price = snapshot.val().TargetPrice
    ticker_name = snapshot.val().TickerName
    stop_loss = snapshot.val().StopLoss
    symbol = snapshot.val().TickerSymbol
    console.log("Symbol ", symbol)

    max_pl = calculate_max_profit(Number(entry_price), Number(entry_price), Number(stop_loss))


    const trade_template =
        `
        <div class="col-md-4">
                            <div class="card h-100 hover-actions-trigger">
                                <div class="card-body pb-1">
                                    <div class="d-flex align-items-center"> <strong>${ticker_name}</strong> </div>
                                    <span class="badge badge-phoenix fs--2 mb-4 badge-phoenix-success"><span
                                            class="badge-label">completed</span></span>
                                    <div class="d-flex align-items-center mb-4">
                                    <!-- TradingView Widget BEGIN -->
                                    <div class="tradingview-widget-container">
                                    <div class="tradingview-widget-container__widget"></div>
                                    <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
                                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
                                    {
                                    "symbol": "NSE:RELIANCE",
                                    "width": "100%",
                                    "colorTheme": "light",
                                    "isTransparent": true,
                                    "locale": "in"
                                    }
                                    </script>
                                    </div>
                                    <!-- TradingView Widget END -->
                                    </div>

                                    <div class="d-flex align-items-center mb-4">
                                        <p class="fw-bold mb-0 lh-1">Entry Price : <span class="ms-1 text-1100">${entry_price}</span>
                                        </p>
                                    </div>

                                    <div class="d-flex align-items-center mb-4">
                                        <p class="fw-bold mb-0 lh-1">Stop Loss : <span class="ms-1 text-1100">${stop_loss}</span>
                                        </p>
                                    </div>

                                    <div class="d-flex align-items-center mb-4">
                                        <p class="fw-bold mb-0 lh-1">Target Price : <span
                                                class="ms-1 text-1100">${target_price}</span>
                                        </p>
                                    </div>

                                    <div class="d-flex justify-content-between text-700 fw-semi-bold">
                                        <p class="mb-2"> Progress</p>
                                        <p class="mb-2 text-1100">100%</p>
                                    </div>
                                    <div class="progress bg-success-100">
                                        <div class="progress-bar rounded bg-success" role="progressbar"
                                            aria-label="Success example" style="width: 100%" aria-valuenow="25"
                                            aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                    
                                    <div class="row align-items-center">
                                        <div class="col-md-7">
                                            <div class="d-flex flex-column mt-4">
                                                <p class="mb-0 fw-bold fs--1">Started :<span class="fw-semi-bold text-600 ms-1"> 17th Nov. 2020</span></p>
                                                <p class="mb-0 fw-bold fs--1">Max Loss :<span class="fw-semi-bold text-600 ms-1 text-danger"> ${max_pl[0]}%</span></p>
                                                <p class="mb-0 fw-bold fs--1">Max Profit :<span class="fw-semi-bold text-600 ms-1 text-success"> ${max_pl[1]}%</span></p>
                                            </div>
                                        </div>
                                        
                                    </div>
                                    

                                    <hr>
                                    <div class="row">
                                    <div class="col-md-12">
                                        <div class="d-flex justify-content-center m-2">
                                            <button type="button" data-bs-toggle="modal"
                                                class="btn btn-lg btn-success execute_trade_modal"
                                                data-bs-target="#verticallyCentered" aria-label="{{t.id}}"
                                                id="">Execute</button>
                                        </div>
                                    </div>

                                </div>

                                </div>
                            </div>
                        </div>
        `
    console.log(trade_template)
    trades_main_wrapper.prepend(trade_template)

})


function change_quantity() {
    $("#quantity_param").on("change", function () {
        console.log("Here is ")
    })
}
