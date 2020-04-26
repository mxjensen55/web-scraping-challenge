from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo=PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars=mongo.db.mars
    mars_info=scrape_mars.scrape()
    mars.update({}, mars_info, upsert=True)
    return redirect("/", code=302)
    

if __name__=="main":
    app.run(debug=True)
   