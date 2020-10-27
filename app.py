from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_DB")
.
@app.route("/")
def home():

    mars_info = mongo.db.mars_data.find_one()
    
    return render_template("index.html", mars_data=mars_info)

@app.route("/scrape")
def scraper():

    mars_info = mongo.db.mars_info

    mars_data = scrape_mars.scrape()

    mars_info.update({}, mars_data, upsert=True)

    return "scraping was successful"


if __name__ == "__main__":
    app.run(debug=True)