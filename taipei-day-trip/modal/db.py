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