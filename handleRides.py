from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
uri = os.getenv("URI")
client = MongoClient(uri)

db = client.get_database("carpool")

# Takes in ride data and creates a ride document on db
# Ride id will be stored under the user's rides.
def post_ride(destination, origin, day, arrival, car, member):
    # find where to store data
    rides = db.get_collection("rides")
    date = datetime.datetime.now()
    dateString = date.strftime("%Y-%m-%d %H:%M:%S")

    # data entry
    result = rides.insert_one(
        {
            "destination": destination,
            "origin": origin,
            "day": day,
            "arrival": arrival,
            "car": car,
            "members": member,
            "date": {
                "created": dateString,
                "last": dateString
            },
        }
    )
    return result

def get_rides(id):

    return ""
