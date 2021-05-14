from flask import *
import mysql.connector
import math
from config import Config
from flask import session

app = Flask(__name__)
app.secret_key = "abcdefghijk"
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

mydb = mysql.connector.connect(
    host="localhost",
    user=Config.db_user,
    password=Config.db_password,
    database="Attraction"
)

userdb = mysql.connector.connect(
    host="localhost",
    user=Config.db_user,
    password=Config.db_password,
    database="User"
)

mycursor = userdb.cursor()
mycursor.execute(
    "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),email VARCHAR(255),password VARCHAR(255))")

# Pages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/api/attractions")
def attractions():
    page = int(request.args.get("page", 0))
    keyword = request.args.get("keyword", None)
    if keyword == None:
        try:
            mycursor = mydb.cursor()
            # 資料庫筆數
            mycursor.execute("SELECT COUNT(*) FROM attractions")
            count = mycursor.fetchone()
            count = count[0]
            # 每頁12筆資料的總頁數
            totalPage = math.ceil(count/12)-1
            mycursor.execute(
                "SELECT * FROM attractions LIMIT 12 OFFSET {}".format(page*12))
            myresult = mycursor.fetchall()
            result = []
            for x in myresult:
                y = {
                    "id": x[0],
                    "name": x[1],
                    "category": x[2],
                    "description": x[3],
                    "address": x[4],
                    "transport": x[5],
                    "mrt": x[6],
                    "latitude": x[7],
                    "longitude": x[8],
                    "images": x[9].split(",")[1:]
                }
                result.append(y)
            if totalPage <= page:
                page = None
                return Response(json.dumps({
                    "nextPage": page,
                    "data": result
                }, sort_keys=False), mimetype="application/json")
            else:
                return Response(json.dumps({
                    "nextPage": page+1,
                    "data": result
                }, sort_keys=False), mimetype="application/json")
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500
    else:
        try:
            mycursor = mydb.cursor()
            # keyword總筆數
            mycursor.execute(
                "SELECT COUNT(*) FROM attractions WHERE name Like '%{}%'".format(keyword))
            count = mycursor.fetchone()
            count = count[0]
            # 每頁12筆資料的總頁數
            totalPage = math.ceil(count/12)-1
            mycursor.execute(
                "SELECT * FROM attractions WHERE name Like '%{}%' LIMIT 12 OFFSET {}".format(keyword, page*12))
            myresult = mycursor.fetchall()
            result = []
            for x in myresult:
                y = {
                    "id": x[0],
                    "name": x[1],
                    "category": x[2],
                    "description": x[3],
                    "address": x[4],
                    "transport": x[5],
                    "mrt": x[6],
                    "latitude": x[7],
                    "longitude": x[8],
                    "images": x[9].split(",")[1:]
                }
                result.append(y)
            if totalPage <= page:
                page = None
                return Response(json.dumps({
                    "nextPage": page,
                    "data": result
                }, sort_keys=False), mimetype="application/json")
            else:
                return Response(json.dumps({
                    "nextPage": page+1,
                    "data": result
                }, sort_keys=False), mimetype="application/json")
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500


@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    try:
        attractionId = int(attractionId)
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * FROM attractions WHERE id = '{}'".format(attractionId))
        myresult = mycursor.fetchone()
        if myresult != None:
            result = {
                "id": myresult[0],
                "name": myresult[1],
                "category": myresult[2],
                "description": myresult[3],
                "address": myresult[4],
                "transport": myresult[5],
                "mrt": myresult[6],
                "latitude": myresult[7],
                "longitude": myresult[8],
                "images": myresult[9].split(",")[1:]
            }
            return Response(json.dumps({
                "data": result
            }, sort_keys=False), mimetype="application/json")
        else:
            return Response(json.dumps({
                "error": True,
                "message": "景點編號不正確"
            }, sort_keys=False), mimetype="application/json"), 400
    except:
        return Response(json.dumps({
            "error": True,
            "message": "伺服器內部錯誤"
        }, sort_keys=False), mimetype="application/json"), 500


@app.route("/api/user", methods=["GET", "POST", "PATCH", "DELETE"])
def api_user():
    if request.method == "GET":
        loginState = session.get("signin")
        if loginState != None:
            mycursor = userdb.cursor()
            mycursor.execute(
                "SELECT id,name,email FROM users WHERE email = '{}'".format(loginState))
            myresult = mycursor.fetchone()
            return Response(json.dumps({
                "data": {
                    "id": myresult[0],
                    "name": myresult[1],
                    "email": myresult[2]
                }
            }, sort_keys=False), mimetype="application/json")
        if loginState == None:
            return Response(json.dumps({
                "data": None
            }, sort_keys=False), mimetype="application/json")
    elif request.method == "POST":
        try:
            data = request.get_json()
            registerName = data["name"]
            registerEmail = data["email"]
            registerPassword = data["password"]
            mycursor = userdb.cursor()
            mycursor.execute(
                "SELECT email FROM users WHERE email = '{}'".format(registerEmail))
            myresult = mycursor.fetchone()
            if myresult != None:
                return Response(json.dumps({
                    "error": True,
                    "message": "此電子郵件已註冊過帳戶"
                }, sort_keys=False), mimetype="application/json"), 400
            if myresult == None:
                ins = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                val = (registerName, registerEmail, registerPassword)
                mycursor.execute(ins, val)
                userdb.commit()
                return Response(json.dumps({
                    "ok": True
                }, sort_keys=False), mimetype="application/json")
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500

    elif request.method == "PATCH":
        try:
            data = request.get_json()
            loginEmail = data["email"]
            loginPassword = data["password"]
            mycursor = userdb.cursor()
            mycursor.execute(
                "SELECT email,password FROM users WHERE email = '{}'".format(loginEmail))
            myresult = mycursor.fetchone()
            if myresult != None and myresult[1] == loginPassword:
                session["signin"] = myresult[0]
                session.permanent = True
                return Response(json.dumps({
                    "ok": True,
                }, sort_keys=False), mimetype="application/json")
            else:
                return Response(json.dumps({
                    "error": True,
                    "message": "電子郵件或密碼輸入錯誤"
                }, sort_keys=False), mimetype="application/json"), 400
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500
    elif request.method == "DELETE":
        session.clear()
        return Response(json.dumps({
            "ok": True,
        }, sort_keys=False), mimetype="application/json")


app.run(host="0.0.0.0", port=3000, debug=True)
