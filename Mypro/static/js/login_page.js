$(function () {
    let user_flag = 0;
    let pass_flag = 0;
    $("#close_win").on("click", function () {
        parent.document.getElementById("shade").classList.add("hide");
        parent.document.getElementById("page").classList.add("hide");
    });

    $('#button1').on("click", function () {
        console.log('button1')
        let username = $("#username").val();
        let password = $("#password").val();
        let alert_string = "";
        if (username == "") {
            alert_string += "请输入用户名!";
        }
        if (password == "") {
            if (alert_string != "") alert_string += "\n";
            alert_string += "请填写密码!";
        }
        if (alert_string.length != 0) {
            window.alert(alert_string);
        } else {

            console.log('before')

            check(username, password)
            console.log(user_flag)
            console.log(pass_flag)
            console.log('end')


        }

    });

    $("#button1").mouseover(function () {
        $(this).attr("class", "button1_ch");
    });
    $("#button1").mouseout(function () {
        $(this).attr("class", "button1");
    });
    $("#button2").mouseover(function () {
        $(this).attr("class", "button2_ch");
    });
    $("#button2").mouseout(function () {
        $(this).attr("class", "button2");
    });

    function check(username, password) {
        console.log('check')
        $.ajax({
            type: "POST",
            dataType: "json",


            traditional: true,
            url: "/user/check_user",
            data: {
                "username": username,
                "password": password
            },
            beforeSend: function () {

            },
            success: function (res) {
                console.log('success')
                user_flag = res.user_flag
                pass_flag = res.pass_flag
                if (user_flag == 0 && pass_flag == 0) {
                    window.alert("用户名和密码错误!");
                } else if (user_flag == 0) {
                    window.alert("用户名错误!");
                } else if (pass_flag == 0) {
                    window.alert("密码错误!");
                } else {
                    sessionStorage.setItem("login_status", "1");
                    sessionStorage.setItem("username", username);
                    let item = parent.document.getElementById("login_name");
                    item.innerText = username;
                    parent.document.getElementById("shade").classList.add("hide");
                    parent.document.getElementById("page").classList.add("hide");

                }
                console.log(user_flag)


            },
            error: function () {
                console.log('eorr')
            }
        });
    }


});
