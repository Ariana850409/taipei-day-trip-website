let path = location.pathname;
let url = '/api/' + path;
function attractionData() {
    fetch(url, {})
        .then(res => {
            return res.json();
        }).then(result => {
            console.log(result);
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
    fetch(url, {})
        .then(res => {
            return res.json();
        }).then(result => {
            let morningBtn = document.querySelector("#morning-btn");
            let eveningBtn = document.querySelector("#evening-btn");
            let money = document.querySelector(".money");
            if (n == 0) {
                morningBtn.style.backgroundColor = "#448899";
                eveningBtn.style.backgroundColor = "#FFFFFF";
                money.textContent = "新台幣 2000 元";
            } else if (n == 1) {
                morningBtn.style.backgroundColor = "#FFFFFF";
                eveningBtn.style.backgroundColor = "#448899";
                money.textContent = "新台幣 2500 元";
            }
        }).catch((err) => {
            console.log('錯誤:', err);
        });
}
