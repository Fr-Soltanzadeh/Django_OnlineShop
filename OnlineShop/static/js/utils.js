function refresh_token(fail_url, success_function) {
    const refresh_token_url = "/api/v1/accounts/refresh_token/"
    fetch(refresh_token_url, {
        method: 'GET',
        headers: {
            'Authorization': "Bearer " + window.localStorage.getItem("refresh_token")
        }
    })
        .then(
            response => {
                if (response.ok) {
                    return response.json();
                } else {
                    if (response.status == 401) {
                        delete_token()
                        window.location.href = fail_url;
                    } else {
                        throw new Error('error using refresh token');
                    }
                }
            }
        )
        .then((data) => {
            window.localStorage.setItem("access_token", data.access_token);
            window.localStorage.setItem("refresh_token", data.refresh_token);
            if (success_function) {
                success_function();
            }

        }
        )
}

function fetch_get_authorization(url, use_data, fail_url, success_function) {
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem("access_token")}`
        }
    })
        .then(
            response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    if (response.status == 401) {
                        refresh_token(fail_url, success_function)
                    } else {
                        throw new Error('not connected');
                    }

                }
            }
        )
        .then((data) => {
            use_data(data)
        })
        .catch(function (error) {
            console.log(error);
        });
}

function delete_token() {
    window.localStorage.removeItem("access_token");
    window.localStorage.removeItem("refresh_token");
}

function refresh_page() {
    location.reload()
}


function add_to_cart(product_id) {
    const url = '/api/v1/cart/add/'
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({ product_id: product_id }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${window.localStorage.getItem("access_token")}`,
        }
    })
        .then(
            response => {
                console.log(response.status)
                if (response.ok) {

                    window.location.href = "/cart/";
                }
                else {
                    console.log("refresh")
                    if (response.status == 401) {

                        refresh_token("/accounts/login/", `${add_to_cart(product_id)}`);
                    } else {
                        throw new Error('not connected');
                    }
                }
            }
        )
        .catch(function (error) {
            console.log(error);
        });
}

function post_address(load_address) {
    const url = "/api/v1/accounts/user_addresses/"
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const form = document.getElementById("add_address");
    const formData = new FormData(form);
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${window.localStorage.getItem("access_token")}`,
        }
    })
        .then(
            response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    if (response.status == 401) {
                        refresh_token("/accounts/login/", post_address)
                    } else {
                        throw new Error('not connected');
                    }
                }
            }
        )
        .then((data) => {

            load_address(data)
        })
        .catch(function (error) {
            console.log(error);
        });
}

