from flask import Blueprint, jsonify, json, request
from api.models.message import (
    Message, 
    user_messages,
    check_duplicate_message,
    get_message_record,
    get_inbox_record,
    get_sent_messages,
    get_all_received_messages,
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
            "sender_status": "sent",
            "reciever_status": "unread",
            "receiver": data.get("reciever"),
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
                                "message": "Sent message successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        else:

            response = (
                jsonify(
                    {"status": 409, "error": "Message already sent"}
                ),
                409,
            )

        return response
    

    def get_a_message(self, record_id):
        results = get_message_record(int(record_id))
        response = None
        if results:
            response = jsonify({"status": 200, "data": [results]}), 200
        else:

            response = (
                jsonify(
                    {"status": 404, "error": "Message with such id does not exist"}
                ),
                404,
            )

        return response



    def delete_email(self, inbox_mail_id):
        """ 
        deleting an email from a user's inbox.
        """
        results = get_inbox_record(inbox_mail_id)
        response = None
        if results:
            user_messages.remove(results)
            response = (
                jsonify({
                "status": 200,
                "data": [{
                    "message": "Message successfully deleted."
                }]
            }), 200
            )
        else:
            response = (
                jsonify(
                    {"status": 404, "error": "Message with such id does not exist"}
                ),
                404,
            )

        return response


    def fetch_sent_emails(self, sender_stat):
        """
        Returns all users sent messages.
        """
        sender_id = get_current_identity()
        collection = get_sent_messages(sender_stat, sender_id)
        response = None

        if collection:
            response = (
                jsonify({
                "status": 200,
                "data": [record for record in collection],
                "message": "These are your sent messages"
            }), 200)
            
        else:
            response = (
                jsonify(
                    {"status": 404, "error": "You have not sent any mail yet."
                }), 404
            )
        return response


    def fetch_all_received_emails(self, receiver_stat):
        """
        Returns all user's inbox messages.
        """
        receiver_id = get_current_identity()
        collection = get_all_received_messages(receiver_stat, receiver_id)
        response = None

        if collection:
            response = (
                jsonify({
                "status": 200,
                "data": [record for record in collection],
                "message": "These are your inbox messages"
            }), 200)
            
        else:
            response = (
                jsonify(
                    {"status": 404, "error": "You have not received any mail yet."
                }), 404
            )
        return response
        


          