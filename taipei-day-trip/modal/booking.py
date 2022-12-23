from modal.db import db_connect

# method = GET, 回傳行程資料
def get_trip_by_user_id(user_id):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                SELECT 
                    spots.id,
                    spots.name,
                    spots.address,
                    imgs.url,
                    cart.date,
                    cart.time,
                    cart.price
                FROM cart
                LEFT JOIN spots ON cart.attraction_id = spots.id
                LEFT JOIN imgs ON spots.id = imgs.spot_id
                WHERE user_id = %s AND order_num = '0' 
                GROUP BY spots.id
            '''
            val = (user_id,)
            cursor.execute(sql,val)
            result = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# method = POST, 新增行程資料
def add_trip(user_id,att_id,date,time,price):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                INSERT INTO cart (
                    user_id, 
                    attraction_id, 
                    date,
                    time,
                    price
                )VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    date = %s,
                    time = %s,
                    price = %s
            '''
            val = (user_id, att_id, date, time, price,
                   date, time, price)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result

# method = DELETE, 刪除行程資料
def delete_trip_by_id(user_id, att_id):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                DELETE FROM cart 
                WHERE user_id = %s
                AND attraction_id = %s
                AND order_num = '0'
            '''
            val = (user_id, att_id)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result