from flask import jsonify, request
import json
from api.utilitiez.auth_token import (
    encode_token)
from api.utilitiez.validation import validate_new_user, validate_new_message
from database.db import DatabaseConnection
from api.models.user import User

db = DatabaseConnection()


class UserController():
    """Control logic for communication between user model and view"""

    def signup(self):
        new_user = json.loads(request.data)
        try:
            first_name = new_user["firstname"]
            last_name = new_user["lastname"]
            email = new_user["email"]
            password = new_user["password"]

        except KeyError:
            return (
                jsonify(
                    {
                        "error": "Please provide correct keys for input data",
                        "status": 422,
                    }
                ),
                422,
            )

        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
        error = validate_new_user(**new_user)
        if error:
            return error
        user_exists = db.check_if_user_exists(new_user["email"]
        )
        response = None
        if user_exists:
            response = jsonify({"error": user_exists, "status": 409}), 409
        else:

            new_user_details = db.insert_user(**new_user)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            { 
                                "user": new_user_details,
                                "success": f"{first_name} registered Successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        return response

    def login(self):
        if not request.data:
            return (
                jsonify(
                    {"error": "Please provide valid login data", "status": 400}
                ),
                400,
            )
        # Get user credentials
        user_credentials = json.loads(request.data)
        response = None
        try:
            user_email = user_credentials["email"]
            user_password = user_credentials["password"]

            # submit user details as required
            data = db.is_valid_credentials(user_email, user_password)
            if data:
                response = (
                    jsonify(
                        {
                            "status": 200,
                            "data": [
                                {
                                    "token": encode_token(data["id"], data["email"]),
                                    "success": f"{user_email} logged in successfully",
                                }
                            ],
                        }
                    ),
                    200,
                )
            else:
                response = (
                    jsonify({"error": "Wrong login credentials.", "status": 401}),
                    401,
                )

        except KeyError:
            response = (
                jsonify(
                    {
                        "error": "Please provide the correct keys for the data",
                        "status": 422,
                    }
                ),
                422,
            )
        return response

    def group_message(self, data, grp_id):
        if not request.data:
            return (
                jsonify(
                    {
                        "error": "Please provide details",
                        "status": 400,
                    }
                ),
                400,
            )
        data = request.get_json(force=True)

        group_message_data = {
            "subject": data.get("subject"),
            "message": data.get("message"),
            "sender_status": "sent",
            "receiver_status": "unread",
            "group_id": data.get("groupId"),
        }

        not_valid = validate_new_message(**group_message_data)
        known_group = db.get_group(data.get("groupId"))
        response = None
        if not known_group:
            response = (
                jsonify({
                    "status": 404, 
                    "error": "Group with such Id does not exist."}
                ),
                404,
            )  
        elif not_valid:
            response = not_valid 
           
        else:
            group_message_data["user_id"] = get_current_identity()["email"]
            new_message = db.create_group_message(**group_message_data)

            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "mail": new_message,
                                "message": "Sent message successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        return response
   
