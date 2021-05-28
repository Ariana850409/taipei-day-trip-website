let spotid;
let spotname;
let address;
let image;
let date;
let time;
let price;
async function bookingData() {
    let username;
    let email;
    let loginReady = document.getElementById("login-ready");
    let logoutReady = document.getElementById("logout-ready");
    await fetch('/api/user', {
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
                document.getElementById("main").style.display = "block";
            } else if (result.data.date != null) {
                spotid = result.data.attraction.id;
                spotname = result.data.attraction.name;
                address = result.data.attraction.address;
                image = result.data.attraction.image;
                date = result.data.date;
                time = result.data.time;
                price = result.data.price;
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
                document.getElementById("main").style.display = "block";
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

TPDirect.setupSDK(20451, 'app_UQHnv7ywu9yqCq4QnAYlscEtMcfIqtju3xkdEEFhbVeEFgVtSqzeEA09B2VV', 'sandbox')
let fields = {
    number: {
        element: '#card-number',
        placeholder: '  **** **** **** ****'
    },
    expirationDate: {
        element: '#card-expiration-date',
        placeholder: '  MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: '  CCV'
    }
}
TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'orange'
        },
        'input.ccv': {
            'font-size': '16px'
        },
        'input.expiration-date': {
            'font-size': '16px'
        },
        'input.card-number': {
            'font-size': '16px'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
})
function onSubmit() {
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    // console.log(tappayStatus);
    if (document.getElementById("contact-phone").value == "") {
        document.querySelector(".payment-error").textContent = "請輸入手機號碼"
    } else if (tappayStatus.canGetPrime === false) {
        console.log('can not get prime');
        document.querySelector(".payment-error").textContent = "請確認付款資訊無誤"
        return
    } else if (tappayStatus.canGetPrime === true) {
        TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                console.log('get prime error ' + result.msg);
                document.querySelector(".payment-error").textContent = "付款失敗 "
                return
            }
            // console.log(result);
            console.log('get prime success，prime: ' + result.card.prime);
            let data = {
                "prime": result.card.prime,
                "order": {
                    "price": price,
                    "trip": {
                        "attraction": {
                            "id": spotid,
                            "name": spotname,
                            "address": address,
                            "image": image
                        },
                        "date": date,
                        "time": time
                    },
                    "contact": {
                        "name": document.getElementById("contact-name").value,
                        "email": document.getElementById("contact-email").value,
                        "phone": document.getElementById("contact-phone").value
                    }
                }
            }
            // console.log(data);
            fetch("/api/orders", {
                method: 'POST',
                body: JSON.stringify(data),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
                .then(res => {
                    return res.json();
                }).then(result => {
                    if (result.data != null && result.data.payment.status == 0) {
                        bookingDelete();
                        window.location.href = "/thankyou?number=" + result.data.number;
                    } else if (result.data != null && result.data.payment.status != 0) {
                        document.querySelector(".payment-error").textContent = "付款失敗: " + result.data.payment.message
                    } else if (result.error && result.message == "尚未登入系統") {
                        loginData('login');
                    } else if (result.error && result.message == "訂單建立失敗") {
                        document.querySelector(".payment-error").textContent = "訂單建立失敗"
                    } else if (result.error) {
                        console.log(result.message);
                    }
                });
        })
    }
}
