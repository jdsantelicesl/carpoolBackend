# handles user function such as creating new user and issuing user_id
# given username when a user does not have it.

from flask import Blueprint, jsonify, current_app, request, Response
from userFunctions import create_user
from marshmallow import Schema, fields, validate

user_bp = Blueprint("user", __name__)

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)

user_schema = UserSchema()


@user_bp.route("/createUser", methods=["POST"])
def createUser():
    # unpack data
    data = request.get_json()
    try:
        validated_data = user_schema.load(data)
        username = validated_data.get("username")
        name = validated_data.get("name")
        email = validated_data.get("email")
    except:
        return Response(
            response=jsonify({"message": "bad request"}),
            status=400,
            mimetype="application/json"
        )

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
