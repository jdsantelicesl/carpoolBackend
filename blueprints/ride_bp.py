from flask import Blueprint, jsonify, current_app, request
from userFunctions import *
from handleRides import *
from googleMaps import searchPlace
from bson import ObjectId
from marshmallow import Schema, fields, validate

ride_bp = Blueprint("ride", __name__)

class PostSchema(Schema):
    destination = fields.Str(required=True, validate=validate.Length(min=1))
    origin = fields.Str(required=True, validate=validate.Length(min=1))
    day = fields.Int(required=True, validate=validate.Range(min=1, max=7))
    arrival = fields.Float(required=True, validate=validate.Range(min=0.0, max=24.0))
    car = fields.Bool(required=True)
    member = fields.Str(required=True, validate=validate.Length(min=1))

post_schema = PostSchema()


@ride_bp.route("/post", methods=["POST"])
def ridePost():
    input_data = request.get_json()

    try:
        data = post_schema.load(input_data)
    except:
        return jsonify({"message": "bad request"}), 400

    # place holder, check auth. To do...
    auth = True

    # unpack the object to make sure that it is formatted correctly
    destination = data.get("destination")
    origin = data.get("origin")
    day = data.get("day")
    arrival = data.get("arrival")
    car = data.get("car")
    member = data.get("member")

    if auth:
        try:
            result = post_ride(destination, origin, day, arrival, car, member)
            add_user_rides(ObjectId(member), result.inserted_id)
            user_activity(ObjectId(member))
            return str(result.inserted_id), 200
        except:
            return jsonify({"message": "error posting ride"}), 500
    else:
        return jsonify({"message": "unauthorized token"}), 401


@ride_bp.route("/locFind", methods=["GET"])
def locFind():
    # get the values passed in url. Format: "/locFind?query=<myquery>&lat=<mylat>&long=<mylong>"
    query = request.args.get("query")
    lat = request.args.get("lat")
    long = request.args.get("long")
    print(query)
    try:
        results = searchPlace(query, lat, long)
        return results, 200
    except:
        return "internal server error", 500


@ride_bp.route("/getRides")
def getRides():
    # get the values passed in url. Format: "/locFind?client_id=<id>"
    id = request.args.get("client_id")
    result = get_rides(id)
    return "placeholder"
