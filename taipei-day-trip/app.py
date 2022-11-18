from flask import *
from flask_restful import Api, Resource, request
import db

app=Flask(
    __name__,
    static_folder="static",
    static_url_path="/static" 
)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# Api
class Attractions(Resource):
	def get(self):
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
				imgs = db.merge(img)
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

    
class AttractionId(Resource):
	def get(self, attractionId):
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
			imgs = db.merge(img)
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

class Categories(Resource):
	def get(self):
		try:
			result = db.select_all_attri("category")
			results = list(set(db.merge(result)))
			data = {
				"data": results
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


api.add_resource(Attractions, '/api/attractions')
api.add_resource(AttractionId, '/api/attraction/<int:attractionId>')
api.add_resource(Categories, '/api/categories')
app.run(host="0.0.0.0",port=3000)