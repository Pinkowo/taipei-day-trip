from flask import *
import sys
sys.path.append("..") 
import db

att_blueprints = Blueprint( 'att', __name__ )

@att_blueprints.route('/api/attraction/<int:attractionId>', methods=['GET'])
def AttractionId(attractionId):
    try:
        result = db.select_id(attractionId)
        if result[0] == None:
            raise ValueError("無此景點編號，請重新嘗試")
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
                "images": result[9].split(',')
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