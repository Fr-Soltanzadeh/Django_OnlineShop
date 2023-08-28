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

function post_address() {
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

function load_address(data) {
    addresses = document.getElementById('addresses')
    data.forEach(address => {
        let li = document.createElement('li')
        li.classList.add("mt-3")
        li.id = `li${address.id}`
        let span = document.createElement('span')
        span.innerText = `${address.province}, ${address.city}, ${address.street}, ${address.detail}, ${address.postal_code}`
        li.appendChild(span)

        edit_btn = document.createElement('button')
        edit_btn.innerHTML = 'edit'
        edit_btn.classList.add("ml-3", "profile-toggle")
        edit_btn.style.width = "60px"
        edit_btn.addEventListener('click', function () {
            edit_address_form = document.getElementById("edit_address_form")
            edit_address = document.getElementById("edit_address")
            edit_address_form.querySelector('input[name="street"]').value = address.street;
            edit_address_form.querySelector('input[name="city"]').value = address.city;
            edit_address_form.querySelector('input[name="detail"]').value = address.detail;
            edit_address_form.querySelector('input[name="postal_code"]').value = address.postal_code;
            edit_address_form.querySelector('input[name="province"]').value = address.province;
            edit_address_form.querySelector('input[name="id"]').value = address.id;
            edit_address.style.display = edit_address.style.display === 'none' ? 'block' : 'none';

        });

        li.appendChild(edit_btn)

        delete_btn = document.createElement('button')
        delete_btn.innerHTML = 'delete'
        delete_btn.setAttribute('onclick', `delete_address(${address.id})`)
        delete_btn.classList.add("ml-3")
        delete_btn.style.width = "60px"
        li.appendChild(delete_btn)

        addresses.appendChild(li)
    });
}
