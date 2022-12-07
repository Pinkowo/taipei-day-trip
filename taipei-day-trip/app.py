from flask import *
from flask_restful import Api
from api.attractions import *
from api.user import *

app=Flask(
    __name__,
    static_folder="static",
    static_url_path="/static" 
)
app.register_blueprint(atts_blueprints, url_prefix='/api')
app.register_blueprint(user_blueprints, url_prefix='/api')
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

app.run(host="0.0.0.0",port=3000,debug=True)