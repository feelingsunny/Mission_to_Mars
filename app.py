from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)
#mongo = PyMongo(app, uri=(f'mongodb+srv://YangLiu:Asdfg12345@cluster0-kdojp.mongodb.net/test'))
#mongodb+srv://Yang_Liu:<password>@cluster0-kdojp.mongodb.net/test
from pymongo import MongoClient

client = MongoClient('mongodb://YangLiu:Asdfg12345@localhost:27017/prod-db')
mongo = client['prod-db']

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)