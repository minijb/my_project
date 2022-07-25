function is_logged_in() {
    let login_status = sessionStorage.getItem("login_status");
    console.log(login_status);
    if (login_status && login_status == "1") {
        return true;
    }
    return false;
}

function logout() {
    sessionStorage.setItem("login_status", "0");
    sessionStorage.removeItem("username");
}

function get_username() {
    return sessionStorage.getItem("username")
}


function to_access() {
    if (!is_logged_in()) {
        $(".login_button").click();
    } else {
        window.location.href = '/user/Access_data'
    }
}


function init() {
    if (is_logged_in()) {
        document.getElementById("login_name").innerText = get_username();
    }
}

init();

$(document).ready(function () {
    $(".login_button").on("click", function () {
        if (is_logged_in()) {
            var result = confirm("Are you sure to logout?");
            if (result) {
                logout();
                document.getElementById("login_name").innerText = "Login/Register";
            }
        } else {
            document.getElementById("shade").classList.remove("hide");
            document.getElementById("page").classList.remove("hide");
            console.log("button")
        }

    })


})