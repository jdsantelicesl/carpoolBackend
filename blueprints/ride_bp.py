from flask import Blueprint, jsonify, current_app, request
from userFunctions import add_user_rides
from googleMaps import searchPlace
from bson import ObjectId

ride_bp = Blueprint("ride", __name__)


@ride_bp.route("/post", methods=["POST"])
def ridePost():
    # place holder, check auth. To do...
    auth = True

    if auth:
        try:
            # unpack the object to make sure that it is formatted correctly
            data = request.get_json()
            destination = data.get("destination")
            origin = data.get("origin")
            day = data.get("day")
            arrival = data.get("arrival")
            car = data.get('car')
            member = data.get("member")

            # init client using reference from app.py
            client = current_app.config["MONGO_CLIENT"]
            
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
                    "members": member
                }
            )

            add_user_rides(ObjectId(member), result.inserted_id)
            return str(result.inserted_id), 200
        except:
            return jsonify({"message": "error posting ride"}), 500
    else:
        return jsonify({"message": "unauthorized token"}), 401
    
@ride_bp.route("/locFind", methods=["GET"])
def locFind():
    # get the values passed in url. Format: "/locFind?query=<myquery>&lat=<mylat>&long=<mylong>""
    query = request.args.get('query')
    lat = request.args.get('lat')
    long = request.args.get('long')
    print(query)
    try: 
        results = searchPlace(query, lat, long)
        return results, 200
    except: 
        return "internal server error", 500