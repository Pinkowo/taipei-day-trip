from modal.db import db_connect

# 若資料庫中無此 email 則插入資料庫
lastId = 1
def add_user(name,email,password):
    global lastId
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = "INSERT INTO user \
                (name, email, password) \
                SELECT %s, %s, %s FROM dual \
                WHERE NOT EXISTS \
                (SELECT * FROM user WHERE email = %s)"
            val = (name, email, password, email)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.rowcount
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# 用 email 查找會員資料
def get_user_by_email(email):
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