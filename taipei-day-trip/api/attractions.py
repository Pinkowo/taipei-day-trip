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
            count = db.count_all()
            result = db.select_limit(12,int(page)*12)
        # 有輸入關鍵字
        else:
            count = db.count_category(keyword)
            result = db.select_search(keyword,12,int(page)*12)
        # 計算最後一頁
        endPage = int(count[0] / 12)
        if int(page) >= endPage:
            nextPage = None
        else:
            nextPage = int(page)+1
        # 把12筆資料放入data
        results = []
        for xid, x in enumerate(result):
            img = db.select_imgs(xid+1)
            imgs = img[0][0].split(',')
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
                "images": imgs
            }
            results.append(resultDict)
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