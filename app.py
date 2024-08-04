import os
from dotenv import load_dotenv

from flask import Flask
from pymongo import MongoClient
from blueprints.ride import ride_bp

app = Flask(__name__)

load_dotenv()
uri = os.getenv('URI')
client = MongoClient(uri)

# stores database instance in the session
app.config["MONGO_CLIENT"] = client

# this imports all of the routes in blueprints/ride.py
# the routes will be accesses via "/ride/" + route
app.register_blueprint(ride_bp, url_prefix="/ride")

@app.route("/")
def index():
    try:
        database = client.get_database("carpool")
        users = database.get_collection("users")
        # Query for a movie that has the title 'Back to the Future'
        users.insert_one({"name": "new User"})
        return "success"
    except:
        return "error"

if __name__ == "__main__":
    # this allows for app to run on local wifi, port 5000, and will reflect changes upon save
    # need to change this before deployment or we expose vulnerabilities.
    app.run(host='0.0.0.0', port=5000, debug=True)
