import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pw",
  database="trip"
)

### 景點資料放進 spots 資料表中 ###
# 開啟json，將資料存進val
val=[]
with open('./taipei-attractions.json', 'r', encoding='utf-8') as f:
    allData = json.load(f)
    data = allData['result']['results'] 
    for x in data:
        val.append(
            (x['name'], x['CAT'], x['description'],
            x['address'].replace("  ",""), x['direction'], x['MRT'],
            x['latitude'], x['longitude'])
        )

# 將val存進資料庫
with mydb.cursor() as cursor:
    sql = "INSERT INTO spots (name, category, \
    description, address, transport, mrt, lat, lng) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, val)
    mydb.commit()


### 景點資料放進 imgs 資料表中 ###
# 開啟json，將資料存進val
val=[]
with open('./taipei-attractions.json', 'r', encoding='utf-8') as f:
    allData = json.load(f)
    data = allData['result']['results']
    for xID, x in enumerate(data):
        result = x['file'].split("https")
        del result[0]
        result2 = []
        for yID, y in enumerate(result):
            if y[-3:].lower() != "jpg":
                del y
                continue
            result2.append("https" + y)
            val.append((xID+1, result2[yID]))

# 將val存進資料庫
with mydb.cursor() as cursor:
    sql = "INSERT INTO imgs (spot_id, url) VALUES (%s, %s)"
    cursor.executemany(sql, val)
    mydb.commit()

mydb.close()


### debug專區 ###
# with mydb.cursor() as cursor:
#     sql = "SELECT spots.*, GROUP_CONCAT(imgs.url) \
#     FROM spots LEFT JOIN imgs \
#     ON imgs.spot_id = spots.id WHERE spot_id = 99;"
#     cursor.execute(sql,)
#     result = cursor.fetchall()
# print(result)
# mydb.close()
   

### 比對原 json 檔跟新 json 檔的變數名稱 ###        
# id=PK, name=name(varchar), category=CAT(varchar),
# description=description(varchar),
# address=address(varchar), transport=direction(varchar), mrt=MRT(varchar),
# lat=latitude(int), lng=longitude(int), images=data['file'].split("https")(varchar)