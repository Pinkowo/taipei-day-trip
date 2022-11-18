import mysql.connector

# 將多個 list 合併為一個
def merge(data):
    merge = []
    for x in data:
        merge.append(x[0])
    return merge

# 給出景點表中所有景點的指定屬性 (id、name...etc)
def select_all_attri(attri):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT "+attri+" FROM spots"
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
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM spots \
                WHERE (category = %s) OR (name LIKE %s) \
                LIMIT %s OFFSET %s"
            val = (value,"%"+value+"%",limit,offset)
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
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM spots WHERE id = %s"
            val = (id,)
            cursor.execute(sql,val)
            result = cursor.fetchone()
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
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM spots LIMIT %s OFFSET %s"
            val = (num,offset)
            cursor.execute(sql,val)
            result = cursor.fetchall()
    except:
        print("error")
    finally:
        mydb.close()
        return result

# 查找指定 id 景點的圖片 url
def select_imgs(spot_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT url FROM imgs WHERE spot_id = %s"
            val = (spot_id,)
            cursor.execute(sql,val)
            result = cursor.fetchall()
    except:
        print("error")
    finally:
        mydb.close()
        return result

# 計算景點表中景點的數量 
def count_all():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM spots"
            cursor.execute(sql,)
            result = cursor.fetchone()
    except:
        print("error")
    finally:
        mydb.close()
        return result

# 計算指定類別的數量
def count_category(cat):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bet@7878",
        database="trip"
    )
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM spots WHERE category = %s"
            val = (cat,)
            cursor.execute(sql,val)
            result = cursor.fetchone()
    except:
        print("error")
    finally:
        mydb.close()
        return result