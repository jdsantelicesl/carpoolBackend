import os
from dotenv import load_dotenv

from flask import Flask
from pymongo import MongoClient
from blueprints.ride_bp import ride_bp
from blueprints.user_bp import user_bp

app = Flask(__name__)

load_dotenv()
uri = os.getenv('URI')
client = MongoClient(uri)

# stores database instance in the session
app.config["MONGO_CLIENT"] = client

# this imports all of the routes in blueprints/ride.py
# the routes will be accesses via "/ride/" + route
app.register_blueprint(ride_bp, url_prefix="/ride")
app.register_blueprint(user_bp, url_prefix="/user")

@app.route("/")
def index():
    return "welcome"

if __name__ == "__main__":
    # this allows for app to run on local wifi, port 5000, and will reflect changes upon save
    # need to change this before deployment or we expose vulnerabilities.
    app.run(host='0.0.0.0', port=5000, debug=True)
