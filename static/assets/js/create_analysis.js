
let ticker_input_box = document.getElementById("get_ticker_name")
ticker_input_box.addEventListener("keydown", function(){
    let ticker_string = $(this).val()
    
    if(ticker_string == ''){
        document.getElementById("tickers-box-wrapper").style.display = "none";    
    }
    else{
        document.getElementById("tickers-box-wrapper").style.display = "block";
        search_stock(ticker_string)
    }

})

ticker_input_box.addEventListener("focusout", function(){
    document.getElementById("tickers-box-wrapper").style.display = "none";
})

ticker_input_box.addEventListener("focusin", function(){
    document.getElementById("tickers-box-wrapper").style.display = "block";
})


function search_stock(ticker){
    
    if (ticker.length >= 1){
        $.ajax({
            type:'get',
            url:'/dashboard/get-ticker-name/',
            data:{
                name__icontains:ticker,
            },
            success:function(data){
                let list_ul = document.getElementById("ticker-ul")
                list_ul.innerHTML = "";
                
                $(data).each(function(item){
                    
                    let list_item = document.createElement('li')
                    list_item.setAttribute("class", "p-2")
                    list_item.setAttribute("id", this["id"])
                    list_item.setAttribute("aria-label", this["name"])
        
                    list_item.addEventListener("mouseover", function(){
                        console.log(list_item.getAttribute('aria-label'))
                        ticker_input_box.value = list_item.getAttribute('aria-label')
                        $("#stock_symbol").value = this['symbol']
                        
                    })

                    item_text = this['name']
                    list_item.innerText = this['symbol']+" "+this['name']
                    list_ul.append(list_item)
                })
            }

        })

    }
}


// let ticker_select_btn = $("#floatingSelectTaskTicker")
// $("#floatingSelectTaskTicker").change(function(){
//     if($(this).val() == 2){
//         $("#strike-side-wrapper").show(50);
//     }
//     else{
//         $("#strike-side-wrapper").hide(50);
//     }
// })