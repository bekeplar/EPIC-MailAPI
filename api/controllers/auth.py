from flask import jsonify, request
import json
from api.utilitiez.auth_token import (
    encode_token)
from api.utilitiez.validation import validate_new_user

from api.models.user import User


user_obj = User()


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
        user_exists = user_obj.check_if_user_exists(new_user["email"]
        )
        response = None
        if user_exists:
            response = jsonify({"error": user_exists, "status": 409}), 409
        else:

            new_user_details = user_obj.insert_user(**new_user)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "user": new_user_details,
                                "success": f"{email} registered Successfully",
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
            user_id = user_obj.is_valid_credentials(user_email, user_password)
            if user_id:
                response = (
                    jsonify(
                        {
                            "status": 200,
                            "data": [
                                {
                                    "token": encode_token(user_id),
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
