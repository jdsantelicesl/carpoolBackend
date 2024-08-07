from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("URI")
client = MongoClient(uri)

db = client['carpool']

# Takes in two bson ids
# Adds ride id to respective user
# returns bool based on success
def add_user_rides(user_id, ride_id):
    print("executed")
    users = db['users']
    filter = {'_id': user_id}
    
    # $push appends the field 'rides' within the user doc. It adds the ride id
    update = {'$push': {'rides': ride_id}}

    result = users.update_one(filter, update)
     
    if result.matched_count == 1:
        return True
    else:
        return False

