from modal.db import db_connect

# 給出景點表中所有的 category
def get_all_categories():
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
def get_attraction_with_keyword(value,limit,offset):
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
def get_attraction_by_page(num,offset):
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
def get_attraction_by_id(id):
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