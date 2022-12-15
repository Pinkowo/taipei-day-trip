from flask import *
import sys
sys.path.append("..") 
import modal.booking as db
import jwt
from config import PR_KEY

book_blueprints = Blueprint( 'book', __name__ )

def check_token(func):
    def wrapper():
        try:
            token_type, access_token = request.headers.get('Authorization').split(' ')
            if token_type != 'Bearer' or token_type is None:
                assert False, '未登入系統，拒絕存取'
            else:
                decoded_token = jwt.decode(access_token, PR_KEY, algorithms="HS256")
            return func(decoded_token)
        except AssertionError as msg:
            data = {
                "error": True,
                "message": str(msg)
            }
            res = make_response(jsonify(data),403)
            return res
        except Exception as e:
            print(e)
            data = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            res = make_response(jsonify(data),500)
            return res
    return wrapper

@book_blueprints.route('/booking', methods=['GET','POST','DELETE'])
@check_token
def Booking(user_info):
    try:       
        if request.method == 'GET': 
            result = db.get_trip_by_user_id(user_info['id'])            
            if result == []:
                data = {
                    "data": None
                }
            else:
                items = []
                for x in result:                    
                    item = {
                        "attraction": {
                            "id": x[0],
                            "name": x[1],
                            "address": x[2],
                            "image": x[3]
                        },
                        "date": x[4],
                        "time": x[5],
                        "price": x[6]
                    }
                    items.append(item)
                data = {
                    "data": items
                }               
            res = make_response(jsonify(data),200)  
                 
        if request.method == 'POST':
            attractionId = request.json["attractionId"]
            date = request.json["date"]
            time = request.json["time"]
            price = request.json["price"]           
            db.add_trip(user_info['id'], attractionId, date, time, int(price))            
            data = {
                "ok": True
            }
            res = make_response(jsonify(data),200)
                   
        if request.method == 'DELETE':
            attractionId = request.json["attractionId"]
            db.delete_trip_by_id(user_info['id'],attractionId)                     
            data = {
                "ok": True
            }
            res = make_response(jsonify(data),200)
            
    except ValueError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),400)
    except Exception as e:
        print("error:",e)
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        res = make_response(jsonify(data),500)
    finally:
        return res
