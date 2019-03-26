from flask import jsonify, request, Blueprint
import json
from api.utilitiez.auth_token import (
    encode_token)
from api.utilitiez.responses import duplicate_email
from api.utilitiez.validation import validate_new_user
from api.models.user import (
    User,
    users,
    is_valid_credentials
)



class UserController():

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
        user_exists = [user for user in users if user['email'] == email]
        response = None
        if user_exists:
            response = jsonify({"error": duplicate_email, "status": 409}), 409
        else:

            new_user_details = User(**new_user)
            users.append(new_user_details.__dict__)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "user": new_user_details.__dict__,
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
        # Get user credentials from user input
        user_credentials = json.loads(request.data)
        response = None
        try:
            email = user_credentials["email"]
            user_password = user_credentials["password"]

            # Comfirming whether its a known user
            user_id = is_valid_credentials(email, user_password)
            if user_id:
                response = (
                    jsonify(
                        {
                            "status": 200,
                            "data": [
                                {
                                    "token": encode_token(str(user_id)),
                                    "success": f"{email} logged in successfully",
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



    
