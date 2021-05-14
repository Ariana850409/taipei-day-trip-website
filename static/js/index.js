let getAPI = false;
let nextPage = 0;
let finalPage = -1;
let keyword = "";
function getData() {
    if (getAPI == false) {
        let req = new XMLHttpRequest();
        req.open("get", "/api/attractions?page=" + nextPage + "&keyword=" + keyword);
        req.onload = function () {
            let data = JSON.parse(this.responseText);
            console.log(data)
            nextPage = data.nextPage;
            if (nextPage == null) {
                finalPage = nextPage;
            }
            if (data.data.length == 0) {
                let main = document.querySelector("#main");
                let cell = document.createElement("div");
                cell.textContent = "查無結果";
                main.appendChild(cell);
            }
            if (data.data != null || nextPage != null) {
                for (let i = 0; i < data.data.length; i++) {
                    let spotName = data.data[i].name;
                    let firstPic = data.data[i].images[0];
                    let mrtStation = data.data[i].mrt;
                    let category = data.data[i].category;
                    let ID = data.data[i].id;
                    let main = document.querySelector("#main");
                    let cell = document.createElement("div");
                    cell.className = "box";
                    main.appendChild(cell);
                    let img = document.createElement("img");
                    img.src = firstPic
                    let title = document.createElement("div");
                    title.textContent = spotName;
                    let content = document.createElement("div");
                    title.className = "title";
                    content.className = "content";
                    let spotID = document.createElement("a");
                    spotID.href = "/attraction/" + ID;
                    spotID.appendChild(img);
                    cell.appendChild(spotID);
                    cell.appendChild(title);
                    cell.appendChild(content);
                    let mrt = document.createElement("p");
                    let cat = document.createElement("p");
                    mrt.textContent = mrtStation;
                    cat.textContent = category;
                    content.appendChild(mrt);
                    content.appendChild(cat);
                };
            }
            getAPI = false;
        };
        req.send();
    };
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
            } else if (result.data == null) {
                loginReady.style.display = "block";
                logoutReady.style.display = "none";
            }
        });
};
function bodyScroll(event) {
    let scrollHeight = document.body.scrollHeight;
    let innerHeight = window.innerHeight;
    let scrollTop = document.documentElement.scrollTop + document.body.scrollTop;
    let scrollBottom = scrollHeight - innerHeight - scrollTop;
    if (scrollBottom < 100 && nextPage != finalPage) {
        getData();
        getAPI = true;
    }
}
window.addEventListener("scroll", bodyScroll, false);
function keywordData() {
    nextPage = 0;
    keyword = document.querySelector(".search-bar").value;
    let main = document.querySelector("#main");
    main.innerHTML = "";
    getData();
};


