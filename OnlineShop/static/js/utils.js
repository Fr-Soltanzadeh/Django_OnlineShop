function refresh_token(fail_url, success_function){
    const refresh_token_url ="/api/v1/accounts/refresh_token/"
    fetch(refresh_token_url,{
        method:'GET',
        headers:{
            'Authorization':"Bearer "+  window.localStorage.getItem("refresh_token")
        }
    })
    .then(
        response=>{
            if (response.ok){
                return response.json(); 
            }else{
                if (response.status==401){
                    delete_token()
                    window.location.href = fail_url;
                }else{
                    throw new Error('error using refresh token');
                }
            }
        }
    )
    .then((data)=> {
        window.localStorage.setItem("access_token", data.access_token);
        window.localStorage.setItem("refresh_token", data.refresh_token);
        success_function();
        }
    )
    }

function delete_token(){
    window.localStorage.removeItem("access_token");
    window.localStorage.removeItem("refresh_token");
    }

function add_to_cart(product_id){
    console.log(product_id)
    const url = '/api/v1/cart/add/'
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url,{
        method:'POST',
        body:JSON.stringify({ product_id: product_id }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'Authorization':`Bearer ${window.localStorage.getItem("access_token")}`,
        }
    })
    .then(
        response=>{
            if (response.ok){
                return response.json();
            }
            else  {
                throw new Error('not connected');
            }
        }
    )
    .catch(function(error) {
        console.log(error);
    });
}