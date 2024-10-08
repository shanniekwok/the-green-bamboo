# Port: 5011
# Routes: /requestListing (POST), /requestListingModify/<requestID> (POST), /requestEdits (POST), /requestEditsModify/<requestID> (POST), /requestInaccuracy (POST), /requestReviewStatus/<requestID> (POST)
# Dataclass: RequestListings
# -----------------------------------------------------------------------------------------

import os
import json
import pytz
import data
import s3Images
from bson import json_util
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Request for listing creation
# - Insert entry into the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/requestListing", methods= ['POST'])
def requestListing():
    conn = g.db
    cursor = conn.cursor()
    rawRequest = request.get_json()

    rawRequestName = rawRequest["listingName"]
    cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (rawRequestName,))
    existingBottle = cursor.fetchone()

    if existingBottle is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "Bottle with the same name already exists."
            }
        ), 400

    if rawRequest['photo']:
        rawRequest['photo'] = s3Images.uploadBase64ImageToS3(rawRequest['photo'])

    # Handle nullable foreign keys
    producerId = rawRequest.get('producerID') or None
    userId = rawRequest.get('userID') or None

    try:
        cursor.execute("""
            INSERT INTO "requestListings" (
                "listingName", bottler, "drinkType", "sourceLink", "brandRelation", 
                "reviewStatus", "userID", photo, "originCountry", "producerID", 
                "producerNew", "typeCategory", abv, age, "reviewLink"
            ) VALUES (%s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            rawRequestName,
            rawRequest['bottler'],
            rawRequest['drinkType'],
            rawRequest['sourceLink'],
            rawRequest['brandRelation'],
            rawRequest['reviewStatus'],
            userId,
            rawRequest['photo'],
            rawRequest['originCountry'],
            producerId,
            rawRequest['producerNew'],
            rawRequest['typeCategory'],
            rawRequest['abv'],
            rawRequest['age'],
            rawRequest['reviewLink']
        ))

        conn.commit()
        newRequestId = cursor.fetchone()

        if newRequestId is None:
            raise Exception("Failed to retrieve the new request ID after insert.")

        return jsonify(
            {
                "code": 201,
                "data": {
                    "listingName": rawRequestName,
                    "requestId": newRequestId
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
    finally:
        cursor.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing creation
# - Update entry with specified id from the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Updated), 400 (Duplicate Detected), 500 (Error during update)
@blueprint.route("/requestListingModify/<string:requestID>", methods= ['POST'])
def requestListingModify(requestID):
    conn = g.db
    cursor = conn.cursor()
    rawRequest = request.get_json()

    rawRequestName = rawRequest["listingName"]
    cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (rawRequestName,))
    existingBottle = cursor.fetchone()

    if existingBottle is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "Bottle with the same name already exists."
            }
        ), 400
        

    # If rawRequest has photo, check if existingRequest has photo, delete if found, else upload image to s3 and save image in db
    if rawRequest['photo']:
        cursor.execute('SELECT photo FROM "requestListings" WHERE id = %s', (requestID,))
        existingRequest = cursor.fetchone()

        if existingRequest:
            s3Images.deleteImageFromS3(existingRequest)
        if rawRequest['photo']:
            rawRequest['photo'] = s3Images.uploadBase64ImageToS3(rawRequest['photo'])

    producerId = rawRequest.get('producerID') or None
    userId = rawRequest.get('userID') or None

    try:
        cursor.execute("""
            UPDATE "requestListings"
            SET "listingName" = %s, bottler = %s, "drinkType" = %s, "sourceLink" = %s, "brandRelation" = %s, 
                "reviewStatus" = %s, "userID" = %s, photo = %s, "originCountry" = %s, "producerID" = %s, 
                "producerNew" = %s, "typeCategory" = %s, abv = %s, age = %s, "reviewLink" = %s
            WHERE id = %s;
        """, (
            rawRequestName,
            rawRequest['bottler'],
            rawRequest['drinkType'],
            rawRequest['sourceLink'],
            rawRequest['brandRelation'],
            rawRequest['reviewStatus'],
            userId,
            rawRequest['photo'],
            rawRequest['originCountry'],
            producerId,
            rawRequest['producerNew'],
            rawRequest['typeCategory'],
            rawRequest['abv'],
            rawRequest['age'],
            rawRequest['reviewLink'],
            requestID
        ))

        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "listingName": rawRequestName,
                    "requestId": requestID
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification
# - Insert entry into the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Invalid Listing), 500 (Error during creation)
@blueprint.route("/requestEdits", methods= ['POST'])
def requestEdits():
    conn = g.db
    cur = conn.cursor()
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])

    cur.execute('SELECT * FROM listings WHERE "id" = %s', (rawListingID,))
    existingListing = cur.fetchone()

    if existingListing is None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Linked listing is not valid!"
            }
        ), 400
    
    newRequest = {
        "editDesc": rawRequest["editDesc"],
        "listingID": rawListingID,
        "userID": int(rawRequest["userID"]),
        "brandRelation": rawRequest["brandRelation"],
        "reviewStatus": rawRequest["reviewStatus"],
        "duplicateLink": rawRequest.get("duplicateLink", ''),
        "sourceLink": rawRequest.get("sourceLink", '')
    }

    try:
        # Insert new edit request into the database
        columns = ', '.join(f'"{key}"' for key in newRequest.keys())
        placeholders = ', '.join(['%s'] * len(newRequest))
        sql = f'INSERT INTO "requestEdits" ({columns}) VALUES ({placeholders})'
        
        cur.execute(sql, list(newRequest.values()))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing modification
# - Update entry with specified id from the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Updated), 400 (Invalid Listing), 500 (Error during update)
@blueprint.route("/requestEditsModify/<string:requestID>", methods= ['POST'])
def requestEditsModify(requestID):
    conn = g.db
    cur = conn.cursor()
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])

    cur.execute('SELECT * FROM listings WHERE "id" = %s', (rawListingID,))
    existingListing = cur.fetchone()

    if existingListing is None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Linked listing is not valid!"
            }
        ), 400
    
    newRequest = {
        "editDesc": rawRequest["editDesc"],
        "listingID": rawListingID,
        "userID": int(rawRequest["userID"]),
        "brandRelation": rawRequest["brandRelation"],
        "reviewStatus": rawRequest["reviewStatus"],
        "duplicateLink": rawRequest.get("duplicateLink", ''),
        "sourceLink": rawRequest.get("sourceLink", '')
    }

    try:
        # Insert new edit request into the database
        columns = ', '.join(f'"{key}"' for key in newRequest.keys())
        placeholders = ', '.join(['%s'] * len(newRequest))
        sql = f'UPDATE "requestEdits" SET ({columns}) = ({placeholders}) WHERE id = %s'
        
        cur.execute(sql, list(newRequest.values()) + [requestID])
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification in venue menu
# - Insert entry into the "requestInaccurate" collection. Follows requestInaccuracy dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Duplicate request), 500 (Error during creation)
@blueprint.route("/requestInaccuracy", methods= ['POST'])
def requestInaccuracy():
    conn = g.db
    cur = conn.cursor()
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])
    rawVenueID = int(rawRequest["venueID"])
    rawUserID = int(rawRequest["userID"])

    # Check if inaccuracy request is already submitted for the same bottle for a venue
    cur.execute("""
        SELECT * FROM "requestInaccuracy"
        WHERE "listingId" = %s AND "venueId" = %s AND "userId" = %s;
    """, (rawListingID, rawVenueID, rawUserID))
    existingListing = cur.fetchone()

    if existingListing is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Duplicate request for inaccuracy!"
            }
        ), 400
    
    # Prepare new request
    reportDate = datetime.now(pytz.timezone('Etc/GMT-8'))
    inaccurateReason = rawRequest.get("inaccurateReason", "")

    try:
        cur.execute(
            """
                INSERT INTO "requestInaccuracy" ("listingId", "userId", "venueId", "reportDate", "inaccurateReason", "reviewStatus")
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (rawListingID, rawUserID, rawVenueID, reportDate, inaccurateReason, False)
        )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit review status of a submitted request
# - Update entry with specified id from the specified collection.
# - Possible return codes: 201 (Updated), 500 (Error during update)

@blueprint.route("/requestReviewStatus/<string:requestID>", methods= ['POST'])
def requestReviewStatus(requestID):
    conn = g.db
    cur = conn.cursor()

    updateRequest = request.get_json()
    targetCollection = updateRequest["targetCollection"]
    status = updateRequest["reviewStatus"]

    try:
        if targetCollection == "requestInaccuracy":
            print(f"Handling requestInaccuracy for requestID: {requestID}")

        cur.execute(
            f'UPDATE "{targetCollection}" SET "reviewStatus" = %s WHERE id = %s;',
            (status, requestID)
        )

        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": requestID
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "requestID": requestID
                },
                "message": "An error occurred while updating the review status."
            }
        ), 500
    
    finally:
        cur.close()