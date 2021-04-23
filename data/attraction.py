import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="debian-sys-maint",
    password="IDMC3xtr1aBwTGlq",
    database="Attraction"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE attractions (id INT PRIMARY KEY, name VARCHAR(255),category VARCHAR(255),description TEXT,address TEXT,transport TEXT,mrt VARCHAR(255),latitude FLOAT,longitude FLOAT,images TEXT)")


with open("data/taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)
spotlist = data["result"]["results"]
for spot in spotlist:
    ID = spot["_id"]
    name = spot["stitle"]
    category = spot["CAT2"]
    description = spot["xbody"]
    address = spot["address"]
    address = address.replace(" ", "")
    transport = spot["info"]
    mrt = spot["MRT"]
    latitude = spot["latitude"]
    longitude = spot["longitude"]
    pic = spot["file"].split("http")
    images = ""
    for each in pic:
        if ".jpg" in each or ".JPG" in each or ".png" in each:
            img = "http"+each
            # print(type(img))
            images = images + "," + img
    # print(images)
    ins = "INSERT INTO attractions (id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (ID, name, category, description, address,
           transport, mrt, latitude, longitude, images)
    mycursor = mydb.cursor()
    mycursor.execute(ins, val)
    mydb.commit()


# mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE Attraction")
# mycursor.execute("CREATE TABLE attractions (id INT PRIMARY KEY, name VARCHAR(255),category VARCHAR(255),description TEXT,address TEXT,transport TEXT,mrt VARCHAR(255),latitude FLOAT,longitude FLOAT,images TEXT)")
# for x in mycursor:
# print(x)
# ins = "INSERT INTO attractions (id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# val = (ID, name, category, description, address,
#        transport, mrt, latitude, longitude, images)
# mycursor.execute(ins, val)
# mydb.commit()
# mycursor.execute("SELECT * FROM attractions")
# for x in mycursor:
#     print(x)
