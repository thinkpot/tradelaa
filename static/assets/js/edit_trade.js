function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}



function EditTrade(form_element, url) {
    event.preventDefault();
    var S_DATA = $(form_element).serialize();
    var csrf_token = getCookie('csrftoken')
    console.log(csrf_token, S_DATA)
    $.ajax({
        type: "PATCH",
        url: url,
        data: S_DATA,
        headers: {
        'X-CSRFToken': getCookie('csrftoken')
        },
        
        success: function () {
            // Swal.fire(
            //     'Good Success',
            //     'Successfully Updated',
            //     'success'
            // )
            Swal.fire({
                icon:"success",
                title:"Successfully Updated"
            }).then((result) => {
                window.location.reload();
            })
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


document.getElementById("edit-trade-form-submit").addEventListener("click", function () {
    var create_trade_form_ele = document.getElementById("edit-trade-form")
    var trade_id = create_trade_form_ele.getAttribute('aria-label')
    var create_trade_url = "/dashboard/create-trade-form/"+trade_id+"/"
    EditTrade(create_trade_form_ele, create_trade_url)
})

