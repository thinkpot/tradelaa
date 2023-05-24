
function updateFunds() {
    $.ajax({
        type:"GET",
        url:"https://api.fyers.in/api/v2/funds",
        headers:{
            "Authorization":api_key+":"+getCookie("access_token")
        },
        success: function(res){
            $(".funds-amount").text(res['fund_limit'][0]['equityAmount'])
            $(".funds-avail-amount").text(res['fund_limit'][7]['equityAmount'])
            $(".funds-profit-amount").text(res['fund_limit'][4]['equityAmount'])
        }
    })
}

$(document).ready(function () {
    updateFunds()
})


function AddFundsFyers(){
    /* First Validate UPI */
    $.ajax({
        type:"POST",
        url:"https://api.fyers.in/fundtransfer/dev/validate-vpa"
    })
}



