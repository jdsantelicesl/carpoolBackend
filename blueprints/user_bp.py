# handles user function such as creating new user and issuing user_id
# given username when a user does not have it.

from flask import Blueprint, jsonify, current_app, request

user_bp = Blueprint("user", __name__)


@user_bp.route("/createUser", methods=["POST"])
def createUser():
    # place holder, check auth. To do...
    auth = True

    if auth:
        try:
            # unpack the object to make sure that it is formatted correctly
            data = request.get_json()
            username = data.get("username")
            name = data.get("name")

            # init client using reference from app.py
            client = current_app.config["MONGO_CLIENT"]

            # find where to store data
            db = client.get_database("carpool")
            users = db.get_collection("users")

            # data entry
            result = users.insert_one(
                {
                    "username": username,
                    "name": name,
                }
            )
            return str(result.inserted_id)
        except:
            return jsonify({"message": "error creating user"}), 500
    else:
        return jsonify({"message": "unauthorized token"}), 401
