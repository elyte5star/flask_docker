
function handleErrors(response) {
    console.log(response.status);
    if (response.redirected) {
        window.open(response.url, "_self");
        return false
    }
    return response;
}

//POST request with token
async function postData(url = "", data = {}) {

    let options = {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.token
        },
        body: JSON.stringify(data),
    };
    const response = await fetch(url, options).then(handleErrors);
    return response.json();
}

//POST request without token
async function auxPost(url = "", data = {}) {
    let options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(data),
    };
    const response = await fetch(url, options);
    return response.json();
}



//GET request with token
async function getData(url = "", data = {}) {
    let options = {
        method: "GET",

        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.token
        },
    };
    const response = await fetch(url, options).then(handleErrors);
    return response.json();
}

//GET request without token
async function _getData(url = "", data = {}) {
    let options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"

        },
    };
    const response = await fetch(url, options);
    return response.json();
}

//DELETE request with token
async function deleteData(url) {
    let options = {
        method: "DELETE",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.token
        }
    };
    const response = await fetch(url, options).then(handleErrors);
    return response.json();
}

//PUT request with token
async function putData(url = "", data = {}) {

    let options = {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.token
        },
        body: JSON.stringify(data),
    };
    const response = await fetch(url, options).then(handleErrors);
    return response.json();
}

function display_Entry(index) {
    return (
        '<div class="contact_id">' +
        "</div>\n" +
        '<div class="contact_name">' +
        "Name : " +
        this.name +
        "</div>\n" +
        '<div class="contact_tel">' +
        "Telephone : " +
        this.tel +
        "</div>\n" +
        '<div class="contact_operations">' +
        '<a href="javascript:void(0);" onclick="update_Entry(' +
        index +
        ')"><i class="fa fa-pencil-square-o"></i></a><br />' +
        '<a href="javascript:void(0);" onclick="delete_Entry(' +
        index +
        ')"><i class="fa fa-trash-o"></i></a>' +
        "</div>"
    );
}


async function products() {
    const returned_result = await _getData("./products").then((result) => {
        if (result['success'] === true) {
            result.data.forEach(function (item) {
                console.log(item);

            });

        }

    });

}


async function specialDeals() {
    const returned_result = await _getData("./products/deals").then((result) => {
        if (result['success'] === true) {
            result.data.forEach(function (item) {
                console.log(item);

            });
        }
    });

}

function confirm() {
    let tel = document.getElementById("aux_tel");
    let email = document.getElementById("aux_email");
    let userid = document.getElementById("userid").value;
    let data;
    if (!email || !tel) {
        data = { "email": "known@aon.com", "telephone": "6666666", "userid": userid }
    } else {
        data = { "email": email.value, "telephone": tel.value, "userid": userid };
    }
    auxPost("./orders/confirm", data).then((response_data) => {
        if (response_data['success'] === true) {
            console.log(response_data);
            Swal.fire({
                icon: "success",
                timerProgressBar: true,
                title: "Thanks for shopping with us!",
                showConfirmButton: false,
                timer: 1500,
            });
            return redirect();
        } else {

            return ($("#info2").html("<strong>Wrong!</strong> " + " Failed Operation!"));
        }
    });

}


async function login() {
    let userName = document.getElementById("username").value;
    let passWord = document.getElementById("password").value;
    const data = { "username": userName, "password": passWord };
    if (isUserNameValid(userName)) {
        auxPost("./auth/get_token", data).then((response_data) => {
            if (response_data['success'] === true) {
                let res = response_data["token_data"];
                localStorage.setItem('token', res['access_token']);
                window.open(res['host_url'], "_self");
                console.log(res);
            } else {

                return ($("#info2").html("<strong>Wrong!</strong> " + " Invalid Credentials!"));
            }
        });
    } else {

        return ($("#info2").html("<strong>Wrong!</strong> " + " Invalid letters for username!"));
    }

}
async function logout() {
    getData("/logout").then((result) => {
        if (result["success"] === true) {
            localStorage.removeItem("token");
            redirect("/");
        } else {
            console.log(result);
            return false;
        }
    });
}

async function signUP() {
    let username_ = $("#username_").val().trim();
    let pass = $("#pass").val().trim();
    let pass_ = $("#pass_").val().trim();
    let email = $("#email_").val().trim();

    if (!is_Input_Error(username_, email, pass, pass_)) {
        let obj = { "username": username_, "email": email, "password": pass };
        const res = await auxPost('./users/signup');

        if (res["username"]) {

            Swal.fire({
                icon: "success",
                timerProgressBar: true,
                title: res["username"] + " has been created!",
                showConfirmButton: false,
                timer: 1200,
            });

            $("#info2").empty();
            hide_add_entry("add_entry");
            return true;

        } else if (res["success"] === false) {

            return ($("#info2").html("Email/Username already registered"));

        } else {

            return ($("#info2").html("Couldnt create a user!"));
        }

    }


}




/* Admin functions */
async function users() {
    const returned_result = await getData("./users/all").then((result) => {
        console.log(result);
    });
}

/* Helper functions */

function redirect() {
    window.location.href = "/";
}


function isUserNameValid(username) {
    /* 
      Usernames can only have: 
      - Lowercase Letters (a-z) 
      - Numbers (0-9)
      - Dots (.)
      - Underscores (_)
    */
    const res = /^[a-z0-9_\.]+$/.exec(username);
    const valid = !!res;
    return valid;
}
function hide_update_entry(id) {
    var element = document.getElementById(id);
    element.style.display = "none";
}

function show_update_entry(id) {
    var element = document.getElementById(id);
    element.style.display = "";
}

function hide_add_entry(id) {
    var element = document.getElementById(id);
    element.style.display = "none";
}

function show_add_entry(id) {
    var name = $("#add_name").val(" ");
    var tel = $("#add_tel").val(" ");
    var element = document.getElementById(id);
    element.style.display = "";
}

function is_valid_Tel(tel) {
    var re = /^[0-9()+\-\s]*$/;
    return re.test(tel);
}

function is_valid_letter(name) {
    var re = /^[A-Za-z]+$/;
    return re.test(name);
}

function is_valid_Email(email) {
    return email.match(
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}

function is_Input_Error(name, email = "", password = "", password_ = "") {
    if (name.length == 0) {
        $("#info2").html("<strong>Wrong!</strong> " + " Empty username!");
    }
    else if (password !== password_) {
        $("#info2").html("<strong>Wrong!</strong> " + " Invalid Credentials.Password mismatch!");
    }
    else if (email.length == 0) {
        $("#info2").html("<strong>Wrong!</strong> " + " Empty email field!");
    }
    // check for valid email
    else if (email.length > 0 && !is_valid_Email(email)) {
        $("#info2").html("<strong>Wrong!</strong> " + " Invalid email address!");
    }
    // check for valid letters
    else if (name.length > 0 && !isUserNameValid(name)) {
        $("#info2").html("<strong>Wrong!</strong> " + " Invalid letters for username!");
    }
    // no error
    else {
        return false;
    }
    return true;
}