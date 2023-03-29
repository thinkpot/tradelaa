function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function CreateTrade(form_element, url) {
    event.preventDefault();
    var S_DATA = $(form_element).serialize();
    
    $.ajax({
        type: "POST",
        url: url,
        data: S_DATA,
        success: function () {
            Swal.fire(
                'Good Success',
                'Successfully Trade Created',
                'success'
            )
        },
        error:function(e){
            let error_list = e.responseText
            let error_text = ''
            console.log(JSON.parse(error_list))
            
            $.each(JSON.parse(error_list), function(index, jsonObject){
                error_text += index+"->"+jsonObject[0]
                
            })
            console.log(error_text)
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: error_text,
              })
        }
        

    })
}


document.getElementById("create-trade-form-submit").addEventListener("click", function () {
    var create_trade_form_ele = document.getElementById("create-trade-form")
    var create_trade_url = "/dashboard/create-trade-form/"
    CreateTrade(create_trade_form_ele, create_trade_url)
})

