from flask import *
import sys
sys.path.append("..") 
import db

atts_blueprints = Blueprint( 'atts', __name__ )

@atts_blueprints.route('/api/attractions', methods=['GET'])
def Attractions():
    try:
        page = request.args.get('page')
        keyword = request.args.get('keyword')
        if page == None:
            raise ValueError("請輸入 page")
        if int(page) < 0:
            raise ValueError("頁碼最小值為 0")
        # 沒有輸入關鍵字
        if keyword == None: 
            result = db.select_limit(13,int(page)*12)
        # 有輸入關鍵字
        else:
            result = db.select_search(keyword,13,int(page)*12)
        # 把12筆資料放入data
        results = []
        for x in result:
            resultDict = {
                "id": x[0],
                "name": x[1],
                "category": x[2],
                "description": x[3],
                "address": x[4],
                "transport": x[5],
                "mrt": x[6],
                "lat": x[7],
                "lng": x[8],
                "images": x[9].split(',')
            }
            results.append(resultDict)
        # 判斷最後一頁
        if len(result) < 13:
            nextPage = None
        else:
            nextPage = int(page)+1
            del results[-1]
        data = {
                "nextPage": nextPage,
                "data": results
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