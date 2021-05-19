function bookingData() {
    let username;
    let email;
    loginReady = document.getElementById("login-ready");
    logoutReady = document.getElementById("logout-ready");
    fetch('/api/user', {
        method: 'GET',
    })
        .then(res => {
            return res.json();
        }).then(result => {
            if (result.data != null) {
                loginReady.style.display = "none";
                logoutReady.style.display = "block";
                username = result.data.name;
                email = result.data.email;
            } else if (result.data == null) {
                loginReady.style.display = "block";
                logoutReady.style.display = "none";
            }
        });

    fetch('/api/booking', {
        method: 'GET',
    })
        .then(res => {
            return res.json();
        }).then(result => {
            if (result.error) {
                window.location.href = "/";
            } else if (result.data.date == null) {
                main = document.getElementById("main");
                main.innerHTML = "";
                let cell = document.createElement("div");
                cell.className = "booking";
                let heading = document.createElement("p");
                heading.className = "heading heading-1";
                heading.textContent = "您好，" + username + "，待預訂的行程如下：";
                main.appendChild(cell);
                cell.appendChild(heading);
                let content = document.createElement("p");
                content.textContent = "目前沒有任何待預訂的行程";
                cell.appendChild(content);
            } else if (result.data.date != null) {
                let spotname = result.data.attraction.name;
                let address = result.data.attraction.address;
                let image = result.data.attraction.image;
                let date = result.data.date;
                let time = result.data.time;
                let price = result.data.price;
                document.getElementById("booking-img").src = image;
                document.querySelector(".heading-1").textContent = "您好，" + username + "，待預訂的行程如下：";
                document.getElementById("booking-title").textContent = "台北一日遊：" + spotname;
                document.getElementById("booking-date").textContent = date;
                if (time == "morning") {
                    document.getElementById("booking-time").textContent = "早上 9 點到下午 4 點";
                } else if (time == "afternoon") {
                    document.getElementById("booking-time").textContent = "下午 2 點到晚上 9 點";
                }
                document.getElementById("booking-price").textContent = "新台幣 " + price + " 元";
                document.getElementById("booking-address").textContent = address;
                document.getElementById("contact-name").value = username;
                document.getElementById("contact-email").value = email;
                document.getElementById("check-price").textContent = "總價：新台幣 " + price + " 元";
            }
        });
}

function bookingDelete() {
    fetch('/api/booking', {
        method: 'DELETE',
    })
        .then(res => {
            return res.json();
        }).then(result => {
            if (result.error) {
                loginData('login');
            } else if (result.ok) {
                bookingData();
            }
        });
}
