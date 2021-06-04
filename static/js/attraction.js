let path = location.pathname;
let url = '/api/' + path;
let attractionId;
let today;
function attractionData() {
    fetch(url, {})
        .then(res => {
            return res.json();
        }).then(result => {
            // console.log(result);
            attractionId = result.data.id;
            let firstPic = result.data.images[0];
            let pics = result.data.images;
            let picnum = pics.length;
            let name = result.data.name;
            let category = result.data.category;
            let mrt = result.data.mrt;
            let description = result.data.description;
            let address = result.data.address;
            let transport = result.data.transport;
            let spotImg = document.querySelector(".spotImg");
            spotImg.src = firstPic;
            let spotTitle = document.querySelector(".spotTitle");
            spotTitle.textContent = name;
            let spotMrt = document.querySelector(".spotMrt");
            spotMrt.textContent = category + " at " + mrt;
            let spotDesc = document.querySelector(".spotDesc");
            spotDesc.textContent = description;
            let spotAdd = document.querySelector(".spotAdd");
            spotAdd.textContent = address;
            let spotTrans = document.querySelector(".spotTrans");
            spotTrans.textContent = transport;
            let dots = document.querySelector(".dots");
            for (let i = 0; i < picnum - 1; i++) {
                let dot = document.createElement("li");
                dot.className = "dot";
                dot.style.backgroundColor = "white";
                dots.appendChild(dot);
            }
        }).catch((err) => {
            console.log('錯誤:', err);
        });
    let loginReady = document.getElementById("login-ready");
    let logoutReady = document.getElementById("logout-ready");
    fetch('/api/user', {
        method: 'GET',
    })
        .then(res => {
            return res.json();
        }).then(result => {
            if (result.data != null) {
                loginReady.style.display = "none";
                logoutReady.style.display = "block";
            } else if (result.data == null) {
                loginReady.style.display = "block";
                logoutReady.style.display = "none";
            }
        });
    function minDate() {
        let date_now = new Date();
        let year = date_now.getFullYear();
        let month = date_now.getMonth() + 1;
        if (month < 10) {
            month = "0" + month;
        }
        let date = date_now.getDate();
        if (date < 10) {
            date = "0" + date;
        }
        today = year + "-" + month + "-" + date
        document.querySelector('.date').setAttribute('min', today);
    }
    minDate();
}


let index = 0;
function changePic(n) {
    fetch(url, {})
        .then(res => {
            return res.json();
        }).then(result => {
            let pics = result.data.images;
            let picnum = pics.length;
            let spotImg = document.querySelector(".spotImg");
            let alldots = document.querySelectorAll(".dot");
            let loader = document.querySelector(".loader");
            loader.hidden = false;
            for (let i = 0; i < picnum; i++) {
                alldots[i].style.backgroundColor = "white";
            }
            index += n;
            if (index >= picnum) {
                index = 0;
            } else if (index < 0) {
                index = picnum - 1;
            }
            let choosePic = result.data.images[index];
            let chooseDot = alldots[index]
            spotImg.src = choosePic;
            spotImg.onload = function () {
                loader.hidden = true;
                console.log("onload");
            }
            chooseDot.style.backgroundColor = "black";
        }).catch((err) => {
            console.log('錯誤:', err);
        });
}


function changeTime(n) {
    let morningBtn = document.querySelector("#morning-btn");
    let afternoonBtn = document.querySelector("#afternoon-btn");
    let money = document.querySelector(".money");
    if (n == 0) {
        morningBtn.style.backgroundColor = "#448899";
        afternoonBtn.style.backgroundColor = "#FFFFFF";
        money.textContent = "新台幣 2000 元";
    } else if (n == 1) {
        morningBtn.style.backgroundColor = "#FFFFFF";
        afternoonBtn.style.backgroundColor = "#448899";
        money.textContent = "新台幣 2500 元";
    }
}


function bookingStart() {
    let date = document.querySelector(".date").value;
    let time_obj = document.getElementsByName("time");
    let time = "";
    for (let i = 0; i < time_obj.length; i++) {
        if (time_obj[i].checked) {
            time = time_obj[i].value;
        }
    }
    if (document.querySelector('[name=time]:checked') == null) {
        time = "morning"
    }
    let price;
    if (time == "morning") {
        price = 2000;
    } else if (time == "afternoon") {
        price = 2500;
    }
    if (date == "") {
        document.querySelector(".nodate").style.display = "block";
    } else if (date < today) {
        document.querySelector(".nodate").textContent = "請勿選取先前日期";
        document.querySelector(".nodate").style.display = "block";
    } else if (date >= today && date != "") {
        document.querySelector(".nodate").style.display = "none";
        let data = {
            "attractionId": attractionId,
            "date": date,
            "time": time,
            "price": price
        }
        if (attractionId != null && date != "" && time != null && price != null) {
            fetch('/api/booking', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
                .then(res => {
                    return res.json();
                }).then(result => {
                    console.log(result);
                    if (result.error && result.message == "尚未登入系統") {
                        loginData('login');
                    } else if (result.ok) {
                        window.location.href = "/booking";
                    } else if (result.error) {
                        console.log(result.message);
                    }
                });
        }
    }
}
