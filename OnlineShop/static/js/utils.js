function refresh_token(fail_url){
    const refresh_token_url ="/refresh_token/api/v1/"
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
        location.reload();
        }
    )
    }

function delete_token(){
    window.localStorage.removeItem("access_token");
    window.localStorage.removeItem("refresh_token");
}