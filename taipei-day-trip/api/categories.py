from flask import *
import sys
sys.path.append("..") 
import db

cat_blueprints = Blueprint( 'cat', __name__ )

@cat_blueprints.route('/api/categories', methods=['GET'])
def Categories():
    try:
        result = db.select_cat()
        data = {
            "data": result[0][0].split(',')
        }
        res = make_response(jsonify(data),200)
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        res = make_response(jsonify(data),500)
    finally:
        return res 