from flask import *
from flask_bcrypt import Bcrypt
import jwt
import sys
sys.path.append("..") 
import db

user_blueprints = Blueprint( 'user', __name__ )
bcrypt = Bcrypt()
private_key = "secretinjapaneseishimitsu"

# 註冊一個新的會員
@user_blueprints.route('/user', methods=['POST'])
def SignUp():
    try:
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        hashed_password = bcrypt.generate_password_hash(password=password)
        
        result = db.insert_user(name,email,hashed_password)
        if result == 0:
            raise ValueError("Email 已被註冊")
        
        data = {
            "ok": result
        }
        res = make_response(jsonify(data),200)
    except ValueError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),400)
    except Exception as e:
        print(e)
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        res = make_response(jsonify(data),500)
    finally:
        return res

# 取得當前登入的會員資訊
# @user_blueprints.route('/user/auth', methods=['GET'])
# def Info():
#     global private_key
#     try:
#         token = request.cookies.get('token')
#         decoded_token = jwt.decode(token, private_key, algorithms="HS256")
#         data = {
#             "data": decoded_token
#         }
#         res = make_response(jsonify(data),200)
#     except:
#         data = {
#             "error": True,
#             "message": "伺服器內部錯誤"
#         }
#         res = make_response(jsonify(data),500)
#     finally:
#         return res
    
# GET 取得當前登入的會員資訊
# PUT 登入 / DELETE 登出會員帳戶
@user_blueprints.route('/user/auth', methods=['GET','PUT','DELETE'])
def SignIn():
    global private_key
    try:
        if request.method == 'GET':
            token = request.cookies.get('token')
            if token == None:
                data = {
                    "data": None
                }
            else:
                decoded_token = jwt.decode(token, private_key, algorithms="HS256")
                data = {
                    "data": decoded_token
                }
            res = make_response(jsonify(data),200)
            
        if request.method == 'PUT':
            email = request.json["email"]
            password = request.json["password"]
            
            result = db.select_user(email)
            if result == None:
                raise ValueError("查無此帳號")
            
            check_pw = bcrypt.check_password_hash(result[3], password)
            if check_pw == False:
                raise ValueError("密碼錯誤")
            
            encoded_token = jwt.encode({"id": result[0],"name": result[1],"email": result[2]},\
                private_key, algorithm="HS256")
            
            data = {
                "ok": True
            }
            res = make_response(jsonify(data),200)
            res.set_cookie('token', encoded_token, max_age=604800)
        
        if request.method == 'DELETE':
            data = {
                "ok": True
            }
            res = make_response(jsonify(data),200)
            res.delete_cookie("token")
    except ValueError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),400)
    except Exception as e:
        print(e)
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        res = make_response(jsonify(data),500)
    finally:
        return res