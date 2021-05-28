let username;
let bookingNumber = window.location.search.substr(8, 17);
async function thankyouData() {
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
            } else if (result.data == null) {
                window.location.href = "/";
            }
        });
    fetch("/api/order/" + bookingNumber)
        .then(res => {
            return res.json();
        }).then(result => {
            console.log(result);
            if (result.data != null) {
                document.querySelector(".number").textContent = '訂單編號:' + bookingNumber;
                document.querySelector(".history-img").src = result.data.trip.attraction.image;
                document.getElementById("booking-title").textContent = "台北一日遊：" + result.data.trip.attraction.name;
                document.getElementById("booking-date").textContent = result.data.trip.date;
                if (result.data.trip.time == "morning") {
                    document.getElementById("booking-time").textContent = "早上 9 點到下午 4 點";
                } else if (result.data.trip.time == "afternoon") {
                    document.getElementById("booking-time").textContent = "下午 2 點到晚上 9 點";
                }
                document.getElementById("booking-address").textContent = result.data.trip.attraction.address;
                document.getElementById("booking-price").textContent = "新台幣 " + result.data.price + " 元";
                document.getElementById("booking-name").textContent = "聯絡姓名：" + result.data.contact.name;
                document.getElementById("booking-email").textContent = "聯絡信箱：" + result.data.contact.email;
                document.getElementById("booking-phone").textContent = "手機號碼：" + result.data.contact.phone;
                document.getElementById("main").style.display = "block";
            } else if (result.error && result.message == "尚未登入系統") {
                loginData('login');
            } else if (result.error) {
                console.log(result.message);
            }
        });
}

async function hisyoryData() {
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
            } else if (result.data == null) {
                window.location.href = "/";
            }
        });
    fetch("/api/history")
        .then(res => {
            return res.json();
        }).then(result => {
            console.log(result);
            if (result.data == "") {
                let booking = document.querySelector(".booking");
                let nohistory = document.createElement("div");
                nohistory.className = "heading";
                nohistory.textContent = "未有歷史訂單資訊";
                booking.appendChild(nohistory);
            }
            if (result.data != "") {
                for (let i = 0; i < result.data.length; i++) {
                    let booking = document.querySelector(".booking");
                    let numberhref = document.createElement("a");
                    numberhref.className = "numberhref";
                    numberhref.textContent = "訂單編號: " + result.data[i].number;
                    numberhref.href = "/thankyou?number=" + result.data[i].number;
                    booking.appendChild(numberhref);
                    let schedule = document.createElement("div");
                    schedule.className = "schedule";
                    booking.appendChild(schedule);
                    let spotID = document.createElement("a");
                    spotID.href = "/attraction/" + result.data[i].trip.attraction.id;
                    schedule.appendChild(spotID);
                    let img = document.createElement("img");
                    img.src = result.data[i].trip.attraction.image;
                    img.className = "history-img";
                    spotID.appendChild(img);
                    let detail = document.createElement("div");
                    detail.className = "detail";
                    schedule.appendChild(detail);
                    let title = document.createElement("div");
                    title.textContent = result.data[i].trip.attraction.name;
                    detail.appendChild(title);
                    let date = document.createElement("div");
                    date.textContent = "日期: " + result.data[i].trip.date;
                    detail.appendChild(date);
                    let time = document.createElement("div");
                    if (result.data[i].trip.time == "morning") {
                        time.textContent = "時間: 早上 9 點到下午 4 點";
                    } else if (result.data[i].trip.time == "afternoon") {
                        time.textContent = "時間: 下午 2 點到晚上 9 點";
                    }
                    detail.appendChild(time);
                    let address = document.createElement("div");
                    address.textContent = "地點: " + result.data[i].trip.attraction.address;
                    detail.appendChild(address);
                    let price = document.createElement("div");
                    price.textContent = "總價: 新台幣 " + result.data[i].price + " 元";
                    detail.appendChild(price);
                    let refund = document.createElement("div");
                    refund.className = "refund";
                    schedule.appendChild(refund);
                    let refundBtn = document.createElement("button");
                    refundBtn.className = "refund-btn";
                    refundBtn.textContent = "退款";
                    refund.appendChild(refundBtn);
                    let refundp = document.createElement("span");
                    refundp.textContent = "退款最晚請於行程開始前48小時辦理，逾期恕不受理";
                    refund.appendChild(refundp);

                };
            } else if (result.error && result.message == "尚未登入系統") {
                loginData('login');
            } else if (result.error) {
                console.log(result.message);
            }
        });

    document.querySelector(".heading").textContent = "您好，" + username + "，您的歷史訂單如下：";
    document.getElementById("main").style.display = "block";

}

