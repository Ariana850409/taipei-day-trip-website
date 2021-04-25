from flask import *
import mysql.connector
import math
from config import Config
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

print(Config.db_user)
print(Config.db_password)
mydb = mysql.connector.connect(
    host="localhost",
    user=Config.db_user,
    password=Config.db_password,
    database="Attraction"
)


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


app.run(host="0.0.0.0", port=3000)
