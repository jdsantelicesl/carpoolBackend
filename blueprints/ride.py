from flask import Blueprint

ride_bp = Blueprint("ride", __name__)

@ride_bp.route("/")
def rideIndex():
    return "ride endpoints"