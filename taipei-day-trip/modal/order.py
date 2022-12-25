from modal.db import db_connect

# 建立訂單 (將 order_num 從 0 更新為訂單編號)
def renew_cart(order_num,user_id):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                UPDATE cart SET order_num = %s 
                WHERE user_id = %s
                AND order_num = '0'
            '''
            val = (order_num,user_id)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.rowcount
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# method = POST, 建立訂單
def add_order(order_num,price,name,email,phone,status):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                INSERT INTO orders (
                    number, 
                    price, 
                    name,
                    email,
                    phone,
                    status
                )VALUES (%s, %s, %s, %s, %s, %s)
            '''
            val = (order_num,price,name,email,phone,status)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.rowcount
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# 查詢訂單總價
def get_orders_sum(order_num):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                SELECT CAST(SUM(price) AS UNSIGNED) 
                FROM cart
                WHERE order_num = %s
            '''
            val = (order_num,)
            cursor.execute(sql,val)
            result = cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# 狀態更新為付款成功
def order_status_success(order_num):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            sql = '''
                UPDATE orders SET status = 1 
                WHERE number = %s
            '''
            val = (order_num,)
            cursor.execute(sql,val)
            mydb.commit()
            result = cursor.rowcount
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result
    
# method = GET, 回傳訂單資訊
def get_order_by_number(user_id,order_num):
    mydb = db_connect()
    try:
        with mydb.cursor() as cursor:
            cursor.execute("SET SESSION group_concat_max_len = 10240;")
            sql = '''
                SELECT orders.*,
                (SELECT CONCAT('[',GROUP_CONCAT(
                    CONCAT('{"attraction": {"id":', spots.id, ','),
                    CONCAT('"name":"', spots.name, '",'),
                    CONCAT('"address":"', spots.address, '",'),
                    CONCAT('"image":"'),
                    (SELECT imgs.url FROM spots 
                        LEFT JOIN imgs ON imgs.spot_id = spots.id
                        ORDER BY spots.id LIMIT 1),
                    CONCAT('"},'),
                    CONCAT('"date":"', cart.date, '",'),
                    CONCAT('"time":"', cart.time, '"}')
                ),']')
                FROM cart
                LEFT JOIN spots ON spots.id = cart.attraction_id
                WHERE cart.attraction_id = spots.id) trip
                FROM orders
                LEFT JOIN cart ON cart.order_num = orders.number
                WHERE user_id = %s AND orders.number = %s
                GROUP BY orders.number
            '''
            val = (user_id,order_num)
            cursor.execute(sql,val)
            result = cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        mydb.close()
        return result