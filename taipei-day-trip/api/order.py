from flask import *
import sys
sys.path.append("..")
import modal.order as db
import requests
from datetime import datetime
from api.user import check_token
from config import TAPPAY_PA_KEY

order_blueprints = Blueprint( 'order', __name__ )

# 建立新的訂單，並完成付款程序
@order_blueprints.route('/orders', methods=['POST'])
@check_token
def NewOrder(user_data):
    try:
        if user_data['data'] == None:
            assert False, '未登入系統，拒絕存取'
            
        user_id = user_data['data']['id']
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(user_id)
        prime = request.json["prime"]
        user_name = request.json["name"]
        user_email = request.json["email"]
        user_phone = request.json["phone"]
        
        # 建立新訂單
        result = db.renew_cart(order_number,user_id)
        if result == 0:
                raise ValueError("訂單建立失敗")
        price_tot = db.get_orders_sum(order_number)[0]
        result = db.add_order(order_number,price_tot,user_name,user_email,user_phone,0)
        if result == 0:
                raise ValueError("訂單建立失敗")

        # 付款程序: post 傳回 TapPay
        result = postTapPay(prime,price_tot,order_number,
            user_phone,user_name,user_email,user_id)
        if result['status'] == 0:
            db.order_status_success(order_number)
        
        data = {
            "data": {
                "number": order_number,
                "payment": {
                    "status": result['status'],
                    "message": result['msg']
                }
            }
        }
        res = make_response(jsonify(data),200)
    except ValueError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),400)
    except AssertionError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),403)
    except Exception as e:
        print(e)
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        res = make_response(jsonify(data),500)
    finally:
        return res
    
# 付款程序: post 傳回 TapPay  
def postTapPay(prime,price_tot,order_number,user_phone,user_name,user_email,user_id):
    try:
        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': TAPPAY_PA_KEY
        }
        data = {
            "prime": prime,
            "partner_key": TAPPAY_PA_KEY,
            "merchant_id": "pinkowo057_CTBC",
            "details":"台北一日遊",
            "amount": price_tot,
            "order_number": order_number,
            "cardholder": {
                "phone_number": user_phone,
                "name": user_name,
                "email": user_email,
                "member_id": user_id
            }
        }
        result = requests.post(url, headers=headers, json=data)
        res = json.loads(result.text)
    except Exception as e:
        print(e)
        result = False
    finally:
        return res

    
# 根據訂單編號取得訂單資訊
@order_blueprints.route('/order/<string:orderNumber>', methods=['GET'])
@check_token
def GetOrder(orderNumber,user_data):
    try:
        if user_data['data'] == None:
            assert False, '未登入系統，拒絕存取'
            
        result = db.get_order_by_number(user_data['data']['id'],orderNumber)

        if result == None:
            data = {
                "data": None
            }
        else:
            trip = eval(result[6])
            data = {
                "data": {
                    "number": result[0],
                    "price": result[1],
                    "trip": trip,
                    "contact": {
                        "name": result[2],
                        "email": result[3],
                        "phone": result[4]
                    },
                    "status": result[5]
                }
            }       
        res = make_response(jsonify(data),200) 
    except AssertionError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),403) 
    except Exception as e:
        print(e)
    finally:
        return res