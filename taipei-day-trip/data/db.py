import mysql.connector
from config import DB_PW

def db_connect():
    mydb = mysql.connector.connect(
        host = "localhost",
        user="root",
        password=DB_PW,
        database="trip"
    )
    return mydb

### attractions ###
# 給出景點表中所有景點的指定屬性 (id、name...etc)
def select_cat():
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT GROUP_CONCAT(DISTINCT category) FROM spots"
            cursor.execute(sql)
            result = cursor.fetchall()
    except:
        print("error")
    finally:
        mydb.close()
        return result

# 關鍵字搜尋
def select_search(value,limit,offset):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            cursor.execute("SET SESSION group_concat_max_len = 10240;")
            sql = "SELECT spots.*, GROUP_CONCAT(imgs.url)\
                FROM spots LEFT JOIN imgs ON imgs.spot_id = spots.id \
                WHERE category = %s OR name LIKE %s \
                GROUP BY spots.id LIMIT %s OFFSET %s"
            val = (value,"%"+value+"%",limit,offset)
            cursor.execute(sql,val)
            result = cursor.fetchall()
    except:
        print("error")
    finally:
        mydb.close()
        return result
    
# 限定筆數搜尋
def select_limit(num,offset):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            cursor.execute("SET SESSION group_concat_max_len = 10240")
            sql = "SELECT spots.*, GROUP_CONCAT(imgs.url)\
                FROM spots LEFT JOIN imgs ON imgs.spot_id = spots.id \
                WHERE spots.id = imgs.spot_id \
                GROUP BY imgs.spot_id LIMIT %s OFFSET %s"
            val = (num,offset)
            cursor.execute(sql,val)
            result = cursor.fetchall()
    except:
        print("error")
    finally:
        mydb.close()
        return result
    
# 查找指定 id
def select_id(id):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            cursor.execute("SET SESSION group_concat_max_len = 10240")
            sql = "SELECT spots.*, GROUP_CONCAT(imgs.url) \
            FROM spots LEFT JOIN imgs \
            ON imgs.spot_id = spots.id WHERE spot_id = %s"
            val = (id,)
            cursor.execute(sql,val)
            result = cursor.fetchone()
    except:
        print("error")
    finally:
        mydb.close()
        return result


### user ###
# 若資料庫中無此 email 則插入資料庫
lastId = 1
def insert_user(name,email,password):
    global lastId
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = "INSERT IGNORE INTO user \
                (name, email, password) VALUES (%s, %s, %s)"
            val = (name, email, password)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.rowcount
            # 避免不連續 id
            if result == 0:
                cursor.execute("ALTER TABLE user \
                     AUTO_INCREMENT = " + str(lastId))
            else:
                lastId = cursor.lastrowid
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# 驗證會員 email 及 password
def select_user(email):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM user \
                WHERE email = %s"
            val = (email,)
            cursor.execute(sql,val)
            result = cursor.fetchone()
    except:
        print("error")
    finally:
        mydb.close()
        return result