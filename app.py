from flask import Flask
from blueprints.ride import ride_bp

app = Flask(__name__)

# this imports all of the routes in blueprints/ride.py
# the routes will be accesses via "/ride/" + route
app.register_blueprint(ride_bp, url_prefix="/ride")

@app.route("/")
def index():
    return "success"

if __name__ == "__main__":
    # this allows for app to run on local wifi, port 5000, and will reflect changes upon save
    # need to change this before deployment or we expose vulnerabilities.
    app.run(host='0.0.0.0', port=5000, debug=True)