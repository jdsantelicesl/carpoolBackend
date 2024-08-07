from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("URI")
client = MongoClient(uri)

db = client["carpool"]

def post_ride(destination, origin, day, arrival, car, member):
    # find where to store data
    db = client.get_database("carpool")
    rides = db.get_collection("rides")

    # data entry
    result = rides.insert_one(
        {
            "destination": destination,
            "origin": origin,
            "day": day,
            "arrival": arrival,
            "car": car,
            "members": member,
        }
    )
    return result
