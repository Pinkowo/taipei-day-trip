import mysql.connector

# 給出景點表中所有景點的指定屬性 (id、name...etc)
def select_cat():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pw",
        database="trip"
    )
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
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pw",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT spots.*, GROUP_CONCAT(imgs.url)\
                FROM spots LEFT JOIN imgs \
                ON imgs.spot_id = spots.id \
                WHERE (category = %s) OR (name LIKE %s)\
                GROUP BY imgs.spot_id LIMIT %s OFFSET %s"
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
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pw",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
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
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pw",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT spots.*, GROUP_CONCAT(imgs.url) \
            FROM spots LEFT JOIN imgs \
            ON imgs.spot_id = spots.id WHERE spot_id = %s;"
            val = (id,)
            cursor.execute(sql,val)
            result = cursor.fetchone()
    except:
        print("error")
    finally:
        mydb.close()
        return result