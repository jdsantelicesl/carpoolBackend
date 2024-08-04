from flask import Blueprint, jsonify, current_app, request

ride_bp = Blueprint("ride", __name__)


@ride_bp.route("/post", methods=["POST"])
def rideIndex():
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
            owner = data.get("owner")

            # init client using reference from app.py
            client = current_app.config["MONGO_CLIENT"]
            
            # find where to store data
            db = client.get_database("carpool")
            users = db.get_collection("rides")

            # data entry
            users.insert_one(
                {
                    "destination": destination,
                    "origin": origin,
                    "day": day,
                    "arrival": arrival,
                    "owner": owner
                }
            )
            return "success", 200
        except:
            return jsonify({"message": "error posting ride"}), 500
    else:
        return jsonify({"message": "unauthorized token"}), 401
