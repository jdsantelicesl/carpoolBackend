from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
uri = os.getenv("URI")
client = MongoClient(uri)

db = client.get_database("carpool")

# creates a user using their name and username and email
# returns a user id.
def create_user(name, username, email):
    # find where to store data
    users = db.get_collection("users")

    date = datetime.datetime.now()
    dateString = date.strftime("%Y-%m-%d %H:%M:%S")

    # data entry
    result = users.insert_one(
        {
            "username": username,
            "name": name,
            "email": email,
            "date": {
                "created": dateString,
                "last": dateString,
            }
        }
    )
    return str(result.inserted_id)

def user_activity(id):
    users = db.get_collection("users")

    date = datetime.datetime.now()
    dateString = date.strftime("%Y-%m-%d %H:%M:%S")

    query_filter = {'_id' : id}
    update = {'$set': {'date.last': dateString}}
    users.update_one(query_filter, update)



# Takes in two bson ids
# Adds ride id to respective user
# returns bool based on success
def add_user_rides(user_id, ride_id):
    print("executed")
    users = db['users']
    query_filter = {'_id': user_id}
    
    # $push appends the field 'rides' within the user doc. It adds the ride id
    update = {'$push': {'rides': ride_id}}

    result = users.update_one(query_filter, update)
     
    if result.matched_count == 1:
        return True
    else:
        return False
