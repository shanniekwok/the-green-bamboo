# Port: 5052
# Routes: /createObservationTag (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.local import LocalProxy

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId

from datetime import datetime

import data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@greenbamboo.wbiambw.mongodb.net/GreenBamboo?retryWrites=true&w=majority"
db = PyMongo(app).db

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Creates an observation tag
# - Insert entry into the "observationTags" collection. Follows observationTag dataclass requirements.
# - Duplicate review check: If an observationTag with the same observationTag, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@app.route("/createObservationTag", methods= ['POST'])
def createObservationTag():
    rawTag = request.get_json()
    print(rawTag)
    rawObservation= rawTag['observationTag']
    # Duplicate listing check: Reject if review with the same observation exists in the database
    existingAccount = db.observationTags.find_one({"observationTag": rawObservation})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "ObservationTag": rawObservation
                },
                "message": "Observation tag already exists."
            }
        ), 400
    
    
    # Insert new review into database
    newAccount = data.observationTags(**rawTag)
    try:
        insertResult = db.observationTags.insert_one(data.asdict(newAccount))

        return jsonify( 
            {   
                "code": 201,
                "data": rawObservation
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "ObservationTag": rawObservation
                },
                "message": "An error occurred creating the observation tag."
            }
        ), 500

# -----------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port = 5052)