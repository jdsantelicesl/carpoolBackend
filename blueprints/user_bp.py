# handles user function such as creating new user and issuing user_id
# given username when a user does not have it.

from flask import Blueprint, jsonify, current_app, request, Response
from userFunctions import create_user

user_bp = Blueprint("user", __name__)


@user_bp.route("/createUser", methods=["POST"])
def createUser():
    # unpack data
    data = request.get_json()
    username = data.get("username")
    name = data.get("name")
    email = data.get("email")

    # place holder, check auth. To do...
    auth = True

    if auth:
        try:
            id = create_user(username, name, email)
            response = {"id": id}
            return Response(
                response=jsonify(response),
                status=200,
                mimetype="application/json",
            )
        except:
            return Response(
                response=jsonify({"message": "error creating user"}),
                status=500,
                mimetype="application/json",
            )
    else:
        return Response(
            response=jsonify({"message": "unauthorized token"}),
            status=401,
            mimetype="application/json",
        )
