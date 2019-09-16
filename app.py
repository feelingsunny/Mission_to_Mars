from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#mongo = PyMongo(app, uri=(f'mongodb+srv://YangLiu:Asdfg12345@cluster0-kdojp.mongodb.net/test'))
#mongodb+srv://Yang_Liu:<password>@cluster0-kdojp.mongodb.net/test


#from pymongo import MongoClient
#client = MongoClient('mongodb://YangLiu:Asdfg12345@localhost:27017/prod-db')
#mongo = client['prod-db']

@app.route('/')
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_data)

@app.route('/scrape')
def fun():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({},mars_data,upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)