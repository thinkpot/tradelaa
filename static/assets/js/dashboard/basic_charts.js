//Get last 7 days list
function get_today_days_list(){
    var result = [];
    for (var i=0; i<=0; i++) {
        var d = new Date();
        d.setDate(d.getDate() - i);
        result.push(d.toISOString().slice(0,10));
    }
    return result;
}


function get_last_7_days_list(){
    var result = [];
    for (var i=0; i<=6; i++) {
        var d = new Date();
        d.setDate(d.getDate() - i);
        result.push(d.toISOString().slice(0,10));
    }
    return result;
}

//Get last 30 days list
function get_last_30_days_list(){
    var result = [];
    for (var i=0; i<=29; i++) {
        var d = new Date();
        d.setDate(d.getDate() - i);
        result.push(d.toISOString().slice(0,10));
    }
    return result;
}


function FilterchartData(date1, date2, type, element, count_element, days_count, days){
    $.ajax({
        type:"GET",
        url: `/dashboard/sl-tp-data/?${type}=1&created_at__date__lte=${date1}&created_at__date__gte=${date2}`,
        dataType:"json",
        success: function(data){
            
            LineChart(element, data[0])
            count_element.innerText = data[0]['count']
            days_count.innerText = "Last " + days + " Days"
        }
    })
}



window.onload = function(){
    //Creating Target Chart
    let profit_chart_element = document.getElementById('target-hit-chart')
    let target_count_element = document.getElementById("target-count") 
    let last_7_days = get_last_7_days_list()
    let target_days_count = document.getElementById("profit-chart-days-count")
    FilterchartData(last_7_days[0], last_7_days[6], "is_target", profit_chart_element, target_count_element, target_days_count, 7)

    //Creating Stop Loss Chart
    let stop_loss_element = document.getElementById("stop-loss-chart")
    let stop_loss_count_element = document.getElementById("stoploss-count")
    let stop_loss_days_count = document.getElementById("stoploss-chart-days-count")
    FilterchartData(last_7_days[0], last_7_days[6], "is_sl", stop_loss_element, stop_loss_count_element, stop_loss_days_count, 7)
}

//Filter chart data
let filter_btn = document.getElementById("select-gross-revenue-month-filter")
filter_btn.addEventListener("change", function(){
    console.log($(this).val()) 
    let days = $(this).val()
    let profit_chart_element = document.getElementById('target-hit-chart')
    let target_count_element = document.getElementById("target-count")
    let target_days_count = document.getElementById("profit-chart-days-count")

    let stop_loss_element = document.getElementById("stop-loss-chart")
    let stop_loss_count_element = document.getElementById("stoploss-count")
    let stop_loss_days_count = document.getElementById("stoploss-chart-days-count")
    if(days==7){
        let date = get_last_7_days_list()
        FilterchartData(date[0], date[6], "is_target", profit_chart_element, target_count_element, target_days_count, days)  

        FilterchartData(date[0], date[6], "is_sl", stop_loss_element, stop_loss_count_element, stop_loss_days_count, days)
    }
    if(days==30){
        let date = get_last_30_days_list()
        FilterchartData(date[0], date[29], "is_target", profit_chart_element, target_count_element, target_days_count, days)

        FilterchartData(date[0], date[29], "is_sl", stop_loss_element, stop_loss_count_element, stop_loss_days_count, days)
    }
    if(days==1){
        console.log("sdasjkdhjkas")
        let date = get_today_days_list()
    
        FilterchartData(date[0], date[0], "is_target", profit_chart_element, target_count_element, target_days_count, days)

        FilterchartData(date[0], date[0], "is_sl", stop_loss_element, stop_loss_count_element, stop_loss_days_count, days)
    }
    
})