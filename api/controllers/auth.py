from flask import jsonify, request, Blueprint
import json
from api.utilitiez.auth_token import (
    encode_token)
from api.utilitiez.validation import validate_new_user
from api.models.user import (
    User,
    users,
    check_user_exists,
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
        user_exists = check_user_exists(
            new_user["first_name"], new_user["last_name"], new_user["email"]
        )
        response = None
        if user_exists:
            response = jsonify({"error": user_exists, "status": 409}), 409
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

    
