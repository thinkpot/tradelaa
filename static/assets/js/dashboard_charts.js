
function LineChart(element, data) {
    console.log("hihi ", data)
    var myChart = echarts.init(element)
    var options;

    options = {
        grid: {show: false},
        xAxis: {
            type: 'category',
            data: data['x_axis'],
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: data['y_axis'],
                type: 'line'
            }
        ]
    };
    myChart.setOption(options);

}



