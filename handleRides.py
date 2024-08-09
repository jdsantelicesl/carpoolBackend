from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
uri = os.getenv("URI")
client = MongoClient(uri)

db = client.get_database("carpool")


# Takes in ride data and creates a ride document on db
# Ride id will be stored under the user's rides.
def post_ride(destination, origin, day, arrival, car, member):
    # find where to store data
    rides = db.get_collection("rides")

    date = datetime.now()

    # data entry
    result = rides.insert_one(
        {
            "destination": destination,
            "origin": origin,
            "day": day,
            "arrival": arrival,
            "car": car,
            "members": member,
            "date": {"created": date, "last": date},
        }
    )
    return result


def get_rides(id, rides):
    current_date = datetime.now()
    month_ago = current_date - timedelta(days=30)

    for ride in rides:

        # upper and lower bounds of arrival constraint
        
        if (ride.arrival + 0.5) > 24:
            timeQuery = {
                "$or": [
                    {"arrival": {"$gte": ride.arrival + 0.5 - 24}},
                    {"arrival": {"$lte": ride.arrival - 0.5}},
                ]
            }
        elif (ride.arrival - 0.5) < 0:
            timeQuery = {
                "$or": [
                    {"arrival": {"$gte": ride.arrival - 0.5 + 24}},
                    {"arrival": {"$lte": ride.arrival + 0.5}},
                ]
            }
        else:
            timeQuery = {"arrival": {"$gte": (ride.arrival - 0.5), "$lte": (ride.arrival + 0.5)}}

        query = {
            "date.last": {"$gte": month_ago},
            "day": ride.day,
            **timeQuery,
        }

    return ""
