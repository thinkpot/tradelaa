let api_key = 'NV1BMN088J-100';

function updateFunds() {
    $.ajax({
        type:"GET",
        url:"https://api.fyers.in/api/v2/funds",
        headers:{
            "Authorization":api_key+":"+getCookie("access_token")
        },
        success: function(res){
            console.log(res)
            $(".funds-amount").text("₹ "+ Number(res['fund_limit'][7]['equityAmount']).toFixed(2))
            $(".clear-balance").text("₹ "+ Number(res['fund_limit'][0]['equityAmount']).toFixed(2))
            $(".real-profit-loss").text("₹ "+ Number(res['fund_limit'][3]['equityAmount']).toFixed(2))
            $(".demat-balance").text("₹ "+ Number(res['fund_limit'][1]['equityAmount']).toFixed(2))
        }
    })
}

$(document).ready(function () {
    updateFunds()
})