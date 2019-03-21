from flask import Blueprint, jsonify, json, request
from api.models.message import (
    Message, 
    user_messages,
    check_duplicate_message,
    ) 
from api.utilitiez.auth_token import (
    token_required,
    get_current_identity,
)
from api.utilitiez.validation import validate_new_message

message_bp = Blueprint("message_bp", __name__, url_prefix="/api/v1"
)


class MessagesController():

    def new_message(self, data):
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

        new_message_data = {
            "subject": data.get("subject"),
            "message": data.get("message"),
            "parent_message_id": data.get("ParentMessageID"),
        }

        not_valid = validate_new_message(**new_message_data)
        response = None

        if not_valid:
            response = not_valid
        elif not check_duplicate_message(
                new_message_data["subject"], new_message_data["subject"], 
        ):
            new_message_data["user_id"] = get_current_identity()
            new_message = Message(**new_message_data)
            user_messages.append(new_message.__dict__)

            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "mail": new_message.__dict__,
                                "message": "Created message successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        else:

            response = (
                jsonify(
                    {"status": 409, "error": "Message already created"}
                ),
                409,
            )

        return response
    