from flask import *
import mysql.connector
import math
import datetime
import requests
from dbutils.pooled_db import PooledDB
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "abcdefghijk"
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

mydbPOOL = PooledDB(
    creator=mysql.connector,  # 使用連結資料庫的模組
    maxconnections=10,  # 連線池允許的最大連線數，0和None表示不限制連線數
    mincached=2,  # 初始化時，連結池中至少建立的空閒的連結，0表示不建立
    maxcached=5,  # 連結池中最多閒置的連結，0和None不限制
    maxshared=0,  # 連結池中最多共享的連結數量，0和None表示全部共享。PS: 無用，因為pymysql和MySQLdb等模組的 threadsafety都為1，所有值無論設定為多少，_maxcached永遠為0，所以永遠是所有連結都共享。
    blocking=True,  # 連線池中如果沒有可用連線後，是否阻塞等待。True，等待；False，不等待然後報錯
    maxusage=None,  # 一個連結最多被重複使用的次數，None表示無限制
    setsession=[],  # 開始會話前執行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服務端，檢查是否服務可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='localhost',
    port=3306,
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database='Attraction',
    charset='utf8'
)

userdbPOOL = PooledDB(
    creator=mysql.connector,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    maxshared=0,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host='localhost',
    port=3306,
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database='User',
    charset='utf8'
)

orderdbPOOL = PooledDB(
    creator=mysql.connector,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    maxshared=0,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host='localhost',
    port=3306,
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database='Booking',
    charset='utf8'
)


# mycursor = orderdb.cursor()
# mycursor.execute(
#     "CREATE TABLE orders (bookingNumber VARCHAR(255) PRIMARY KEY, price INT, spotid INT, spotname VARCHAR(255), address VARCHAR(255), image VARCHAR(255), date VARCHAR(255), time VARCHAR(255), username VARCHAR(255), email VARCHAR(255),phone VARCHAR(255), status INT, loginEmail VARCHAR(255))")

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


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/api/attractions")
def attractions():
    page = int(request.args.get("page", 0))
    keyword = request.args.get("keyword", None)
    if keyword == None:
        try:
            conn = mydbPOOL.connection()
            mycursor = conn.cursor()
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
                    "images": x[9].replace("http", "https").split(",")[1:]
                }
                result.append(y)
                conn.close()
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
            conn = mydbPOOL.connection()
            mycursor = conn.cursor()
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
                    "images": x[9].replace("http", "https").split(",")[1:]
                }
                result.append(y)
                conn.close()
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
        conn = mydbPOOL.connection()
        mycursor = conn.cursor()
        mycursor.execute(
            "SELECT * FROM attractions WHERE id = '{}'".format(attractionId))
        myresult = mycursor.fetchone()
        conn.close()
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
                "images": myresult[9].replace("http", "https").split(",")[1:]
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
            conn = userdbPOOL.connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "SELECT id,name,email FROM users WHERE email = '{}'".format(loginState))
            myresult = mycursor.fetchone()
            conn.close()
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
            if registerName == " " or registerEmail == " " or registerPassword == " " or registerName == None or registerEmail == None or registerPassword == None or "@" not in registerEmail:
                return Response(json.dumps({
                    "error": True,
                    "message": "註冊資料有誤"
                }, sort_keys=False), mimetype="application/json")
            else:
                conn = userdbPOOL.connection()
                mycursor = conn.cursor()
                mycursor.execute(
                    "SELECT email FROM users WHERE email = '{}'".format(registerEmail))
                myresult = mycursor.fetchone()
                if myresult != None:
                    conn.close()
                    return Response(json.dumps({
                        "error": True,
                        "message": "此電子郵件已註冊過帳戶"
                    }, sort_keys=False), mimetype="application/json"), 400
                if myresult == None:
                    ins = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                    val = (registerName, registerEmail, registerPassword)
                    mycursor.execute(ins, val)
                    conn.commit()
                    conn.close()
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
            conn = userdbPOOL.connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "SELECT email,password FROM users WHERE email = '{}'".format(loginEmail))
            myresult = mycursor.fetchone()
            conn.close()
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


@app.route("/api/booking", methods=["GET", "POST", "DELETE"])
def api_booking():
    if request.method == "GET":
        loginState = session.get("signin")
        if loginState != None:
            attractionId = session.get("attractionId")
            date = session.get("date")
            time = session.get("time")
            price = session.get("price")
            conn = mydbPOOL.connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "SELECT id,name,address,images FROM attractions WHERE id = '{}'".format(attractionId))
            myresult = mycursor.fetchone()
            conn.close()
            result = None
            if myresult != None:
                result = {
                    "id": myresult[0],
                    "name": myresult[1],
                    "address": myresult[2],
                    "image": myresult[3].replace("http", "https").split(",")[1]
                }
            return Response(json.dumps({
                "data": {
                    "attraction": result,
                    "date": date,
                    "time": time,
                    "price": price
                }
            }, sort_keys=False), mimetype="application/json")

        if loginState == None:
            return Response(json.dumps({
                "error": True,
                "message": "尚未登入系統"
            }, sort_keys=False), mimetype="application/json"), 403

    elif request.method == "POST":
        try:
            loginState = session.get("signin")
            if loginState != None:
                data = request.get_json()
                attractionId = data["attractionId"]
                date = data["date"]
                time = data["time"]
                price = data["price"]
                if attractionId != None and date != None and time != None and price != None:
                    session["attractionId"] = attractionId
                    session["date"] = date
                    session["time"] = time
                    session["price"] = price
                    session.permanent = True
                    return Response(json.dumps({
                        "ok": True
                    }, sort_keys=False), mimetype="application/json")
                else:
                    return Response(json.dumps({
                        "error": True,
                        "message": "輸入不正確或其他原因"
                    }, sort_keys=False), mimetype="application/json"), 400
            if loginState == None:
                return Response(json.dumps({
                    "error": True,
                    "message": "尚未登入系統"
                }, sort_keys=False), mimetype="application/json"), 403
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500

    elif request.method == "DELETE":
        loginState = session.get("signin")
        if loginState != None:
            session.pop('attractionId', None)
            session.pop('date', None)
            session.pop('time', None)
            session.pop('price', None)
            return Response(json.dumps({
                "ok": True
            }, sort_keys=False), mimetype="application/json")
        if loginState == None:
            return Response(json.dumps({
                "error": True,
                "message": "尚未登入系統"
            }, sort_keys=False), mimetype="application/json"), 403


@app.route("/api/orders", methods=["POST"])
def api_orders():
    try:
        loginState = session.get("signin")
        if loginState != None:
            today = datetime.datetime.now()
            bookingNumber = today.strftime('%Y%m%d%H%M%S%f')[:-3]
            data = request.get_json()
            prime = data["prime"]
            price = data["order"]["price"]
            spotid = data["order"]["trip"]["attraction"]["id"]
            spotname = data["order"]["trip"]["attraction"]["name"]
            address = data["order"]["trip"]["attraction"]["address"]
            image = data["order"]["trip"]["attraction"]["image"]
            date = data["order"]["trip"]["date"]
            time = data["order"]["trip"]["time"]
            contactName = data["order"]["contact"]["name"]
            contactEmail = data["order"]["contact"]["email"]
            contactPhone = data["order"]["contact"]["phone"]
            # payStatus 0:已付款 1:未付款 2:已退款
            payStatus = 1
            checkdate = datetime.datetime.strptime(date, '%Y-%m-%d')
            if checkdate < today or date == " " or date == None:
                return Response(json.dumps({
                    "error": True,
                    "message": "行程日期有誤"
                }, sort_keys=False), mimetype="application/json")
            elif "morning" not in time and "afternoon" not in time:
                return Response(json.dumps({
                    "error": True,
                    "message": "行程時間有誤"
                }, sort_keys=False), mimetype="application/json")
            elif contactName == " " or contactEmail == " " or contactPhone == " " or contactName == None or contactEmail == None or contactPhone == None or "@" not in contactEmail:
                return Response(json.dumps({
                    "error": True,
                    "message": "聯絡資訊有誤"
                }, sort_keys=False), mimetype="application/json")
            else:
                try:
                    conn = orderdbPOOL.connection()
                    mycursor = conn.cursor()
                    ins = "INSERT INTO orders (bookingNumber, price, spotid, spotname, address, image, date, time, username, email, phone, status, loginEmail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (bookingNumber, price, spotid, spotname, address, image,
                           date, time, contactName, contactEmail, contactPhone, payStatus, loginState)
                    mycursor.execute(ins, val)
                    conn.commit()
                    conn.close()
                    # pay by prime request
                    payurl = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
                    payheader = {
                        'x-api-key': os.getenv('partner_key')}
                    paydata = {
                        "prime": prime,
                        "partner_key": os.getenv('partner_key'),
                        "merchant_id": "Ariana0409_TAISHIN",
                        "details": "TapPay Test",
                        "amount": price,
                        "cardholder": {
                            "phone_number": contactPhone,
                            "name": contactName,
                            "email": contactEmail
                        }
                    }
                    payrequest = requests.post(
                        payurl, headers=payheader, json=paydata)
                    payresponse = json.loads(payrequest.text)
                    getstatus = payresponse['status']
                    getmsg = payresponse['msg']
                    gettrade = payresponse['rec_trade_id']
                    if getstatus == 0:
                        conn = orderdbPOOL.connection()
                        mycursor = conn.cursor()
                        mycursor.execute(
                            "UPDATE orders SET status = {},tradeID = '{}' WHERE bookingNumber = '{}'".format(0, gettrade, bookingNumber))
                        conn.commit()
                        conn.close()
                        return Response(json.dumps({
                            "data": {
                                "number": bookingNumber,
                                "payment": {
                                    "status": 0,
                                    "message": "付款成功"
                                }
                            }
                        }, sort_keys=False), mimetype="application/json")
                    else:
                        return Response(json.dumps({
                            "data": {
                                "number": bookingNumber,
                                "payment": {
                                    "status": getstatus,
                                    "message": getmsg
                                }
                            }
                        }, sort_keys=False), mimetype="application/json")
                except:
                    return Response(json.dumps({
                        "error": True,
                        "message": "訂單建立失敗"
                    }, sort_keys=False), mimetype="application/json"), 400
        if loginState == None:
            return Response(json.dumps({
                "error": True,
                "message": "尚未登入系統"
            }, sort_keys=False), mimetype="application/json"), 403
    except:
        return Response(json.dumps({
            "error": True,
            "message": "伺服器內部錯誤"
        }, sort_keys=False), mimetype="application/json"), 500


@app.route("/api/order/<orderNumber>")
def api_order(orderNumber):
    try:
        loginState = session.get("signin")
        if loginState != None:
            conn = orderdbPOOL.connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "SELECT * FROM orders WHERE bookingNumber = '{}'".format(orderNumber))
            myresult = mycursor.fetchone()
            conn.close()
            if myresult != None:
                result = {
                    "number": myresult[0],
                    "price": myresult[1],
                    "trip": {
                        "attraction": {
                            "id": myresult[2],
                            "name": myresult[3],
                            "address": myresult[4],
                            "image": myresult[5]
                        },
                        "date": myresult[6],
                        "time": myresult[7]
                    },
                    "contact": {
                        "name": myresult[8],
                        "email": myresult[9],
                        "phone": myresult[10]
                    },
                    "status": myresult[11]
                }
                return Response(json.dumps({
                    "data": result
                }, sort_keys=False), mimetype="application/json")
            else:
                return Response(json.dumps({
                    "error": True,
                    "message": "系統查無資料"
                }, sort_keys=False), mimetype="application/json")
        if loginState == None:
            return Response(json.dumps({
                "error": True,
                "message": "尚未登入系統"
            }, sort_keys=False), mimetype="application/json"), 403
    except:
        return Response(json.dumps({
            "error": True,
            "message": "伺服器內部錯誤"
        }, sort_keys=False), mimetype="application/json"), 500


@app.route("/api/history", methods=["GET", "DELETE"])
def api_history():
    if request.method == "GET":
        try:
            loginState = session.get("signin")
            if loginState != None:
                conn = orderdbPOOL.connection()
                mycursor = conn.cursor()
                mycursor.execute(
                    "SELECT bookingNumber, price, spotid, spotname, address, image, date, time, status FROM orders WHERE loginEmail = '{}'".format(loginState))
                myresult = mycursor.fetchall()
                result = []
                for x in myresult:
                    if x[8] != 1:
                        y = {
                            "number": x[0],
                            "price": x[1],
                            "trip": {
                                "attraction": {
                                    "id": x[2],
                                    "name": x[3],
                                    "address": x[4],
                                    "image": x[5]
                                },
                                "date": x[6],
                                "time": x[7]
                            },
                            "status": x[8]
                        }
                        result.append(y)
                conn.close()
                return Response(json.dumps({
                    "data": result
                }, sort_keys=False), mimetype="application/json")
            if loginState == None:
                return Response(json.dumps({
                    "error": True,
                    "message": "尚未登入系統"
                }, sort_keys=False), mimetype="application/json"), 403
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500

    elif request.method == "DELETE":
        try:
            data = request.get_json()
            refundNumber = data["refundNumber"]
            conn = orderdbPOOL.connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "SELECT tradeID FROM orders WHERE bookingNumber = '{}'".format(refundNumber))
            myresult = mycursor.fetchone()
            tradeID = myresult[0]
            conn.close()
            if myresult != None:
                # refund request
                refundurl = 'https://sandbox.tappaysdk.com/tpc/transaction/refund'
                refundheader = {
                    'x-api-key': os.getenv('partner_key')}
                refunddata = {
                    "partner_key": os.getenv('partner_key'),
                    "rec_trade_id": tradeID
                }
                refundrequest = requests.post(
                    refundurl, headers=refundheader, json=refunddata)
                refundresponse = json.loads(refundrequest.text)
                getstatus = refundresponse['status']
                getmsg = refundresponse['msg']
                if getstatus == 0:
                    conn = orderdbPOOL.connection()
                    mycursor = conn.cursor()
                    mycursor.execute(
                        "UPDATE orders SET status = {} WHERE tradeID = '{}'".format(2, tradeID))
                    conn.commit()
                    conn.close()
                    return Response(json.dumps({
                        "data": {
                            "number": refundNumber,
                            "payment": {
                                "status": 0,
                                "message": "退款成功"
                            }
                        }
                    }, sort_keys=False), mimetype="application/json")
                else:
                    return Response(json.dumps({
                        "data": {
                            "number": refundNumber,
                            "payment": {
                                "status": getstatus,
                                "message": getmsg
                            }
                        }
                    }, sort_keys=False), mimetype="application/json")
            else:
                return Response(json.dumps({
                    "error": True,
                    "message": "查找退款訂單失敗"
                }, sort_keys=False), mimetype="application/json")
        except:
            return Response(json.dumps({
                "error": True,
                "message": "伺服器內部錯誤"
            }, sort_keys=False), mimetype="application/json"), 500


app.run(host="0.0.0.0", port=3000, debug=True)
