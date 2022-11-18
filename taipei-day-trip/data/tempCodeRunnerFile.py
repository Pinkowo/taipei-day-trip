with mydb.cursor() as cursor:
#     # sql = "SELECT GROUP_CONCAT(imgs.url) \
#     sql = "SELECT imgs.url \
#         FROM spots LEFT JOIN imgs \
#         ON imgs.spot_id = 1"
#     cursor.execute(sql,)
#     result = cursor.fetchall()
#     print(result)
    