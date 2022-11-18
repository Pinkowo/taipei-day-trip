from flask import *
import sys
sys.path.append("..") 
import db

att_blueprints = Blueprint( 'att', __name__ )

@att_blueprints.route('/api/attraction/<int:attractionId>', methods=['GET'])
def AttractionId(attractionId):
    try:
        # 找出景點編號的極限值
        spotId = db.select_all_attri("id")
        limit = db.merge(spotId)
        maxId = max(limit)
        minId = min(limit)
        # 判斷景點編號
        if attractionId > maxId:
            raise ValueError("景點編號過大，請重新嘗試")
        if attractionId < minId:
            raise ValueError("景點編號過小，請重新嘗試")
        # 景點編號在正確範圍內，取出資料放進json
        result = db.select_id(attractionId)
        img = db.select_imgs(attractionId)
        imgs = img[0][0].split(',')
        data = {
            "data": {
                "id": result[0],
                "name": result[1],
                "category": result[2],
                "description": result[3],
                "address": result[4],
                "transport": result[5],
                "mrt": result[6],
                "lat": result[7],
                "lng": result[8],
                "images": imgs    
            }
        }
        res = make_response(jsonify(data),200)
    except ValueError as msg:
        data = {
            "error": True,
            "message": str(msg)
        }
        res = make_response(jsonify(data),400)
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        res = make_response(jsonify(data),500)
    finally:
        return res 