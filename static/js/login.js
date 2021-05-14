function loginData(state) {
    let shadow = document.querySelector(".shadow");
    let login = document.querySelector(".login");
    let register = document.querySelector(".register");
    if (state == "login") {
        shadow.style.display = "block";
        login.style.display = "block";
        register.style.display = "none";
    } else if (state == "register") {
        shadow.style.display = "block";
        register.style.display = "block";
        login.style.display = "none";
    } else if (state == "close") {
        shadow.style.display = "none";
        login.style.display = "none";
        register.style.display = "none";
    } else {
        console.log("error");
    }

}

function register() {
    registerName = document.getElementById("register-name").value;
    registerEmail = document.getElementById("register-email").value;
    registerPassword = document.getElementById("register-password").value;
    registerError = document.getElementById("register-error");
    registerSuccess = document.getElementById("register-success");
    if (registerName.indexOf(" ") != -1 || registerEmail.indexOf(" ") != -1 || registerPassword.indexOf(" ") != -1) {
        registerError.textContent = "請勿輸入空白符號"
        registerError.style.display = "block";
    } else if (registerName != "" && registerEmail != "" && registerPassword != "") {
        let data = {
            "name": registerName,
            "email": registerEmail,
            "password": registerPassword
        };
        let url = '/api/user';
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
            .then(res => {
                return res.json();
            }).then(result => {
                if (result.ok) {
                    registerError.style.display = "none";
                    registerSuccess.style.display = "block";
                } else if (result.error) {
                    registerError.textContent = result.message
                    registerError.style.display = "block";
                    registerSuccess.style.display = "none";
                }
            });

    } else if (registerName == "" || registerEmail == "" || registerPassword == "") {
        registerError.textContent = "請輸入姓名或電子郵件或密碼"
        registerError.style.display = "block";
    }
}

function login() {
    loginEmail = document.getElementById("login-email").value;
    loginPassword = document.getElementById("login-password").value;
    loginError = document.getElementById("login-error");
    if (loginEmail.indexOf(" ") != -1 || loginPassword.indexOf(" ") != -1) {
        loginError.textContent = "請勿輸入空白符號"
        registerError.style.display = "block";
    } else if (loginEmail != "" && loginPassword != "") {
        let data = {
            "email": loginEmail,
            "password": loginPassword
        };
        let url = '/api/user';
        fetch(url, {
            method: 'PATCH',
            body: JSON.stringify(data),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
            .then(res => {
                return res.json();
            }).then(result => {
                if (result.ok) {
                    window.location.reload()
                } else if (result.error) {
                    loginError.textContent = result.message
                    loginError.style.display = "block";
                }
            });

    } else if (loginEmail == "" || loginPassword == "") {
        loginError.textContent = "請輸入電子郵件或密碼"
        loginError.style.display = "block";
    }
}
function logout() {
    fetch('/api/user', {
        method: 'DELETE',
    })
        .then(res => {
            return res.json();
        }).then(result => {
            if (result.ok) {
                window.location.reload()
            }
        });
}
