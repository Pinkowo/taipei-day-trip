from flask import *
import sys
sys.path.append("..")
import re
import modal.user as db
from flask_bcrypt import Bcrypt
import jwt
from config import PR_KEY

user_blueprints = Blueprint( 'user', __name__ )
bcrypt = Bcrypt()

# 註冊一個新的會員
@user_blueprints.route('/user', methods=['POST'])
def SignUp():
    try:
        name = request.json["name"]
        email = request.json["email"]
        if not re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$',email):
            raise ValueError("請輸入正確的 Email 格式")
        password = request.json["password"]
        hashed_password = bcrypt.generate_password_hash(password=password)
        
        result = db.add_user(name,email,hashed_password)
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
    
    
# 裝飾器: 驗證 token
def check_token(func):
    def wrapper(*args, **kwargs):
        try:
            token = request.cookies.get('token')
            if token is None:
                data={
                    "data": None
                }
                kwargs.setdefault('user_data', data)
                return func(*args, **kwargs)
            else:
                decoded_token = jwt.decode(token, PR_KEY, algorithms="HS256")
                data = {
                    "data": decoded_token
                }
                kwargs.setdefault('user_data', data)
                return func(*args, **kwargs)
        except Exception as e:
            print(e)
            data = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            res = make_response(jsonify(data),500)
            return res 
    wrapper.__name__ = func.__name__
    return wrapper

# GET 取得當前登入的會員資訊
@user_blueprints.route('/user/auth', methods=['GET'])
@check_token
def Auth_Get(user_data):
    res = make_response(jsonify(user_data),200)
    return res

# PUT 登入 / DELETE 登出會員帳戶
@user_blueprints.route('/user/auth', methods=['PUT','DELETE'])
def Auth():
    try:    
        if request.method == 'PUT':
            email = request.json["email"]
            if not re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$',email):
                raise ValueError("請輸入正確的 Email 格式")
            password = request.json["password"]
            
            result = db.get_user_by_email(email)
            if result == None:
                raise ValueError("查無此帳號")
            
            check_pw = bcrypt.check_password_hash(result[3], password)
            if check_pw == False:
                raise ValueError("密碼錯誤")
            
            encoded_token = jwt.encode({"id": result[0],"name": result[1],"email": result[2]},\
                PR_KEY, algorithm="HS256")
            
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