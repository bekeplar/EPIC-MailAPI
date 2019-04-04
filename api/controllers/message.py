from flask import jsonify, request
from database.db import DatabaseConnection
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.validation import validate_new_message


db = DatabaseConnection()


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
            "sender_status": "sent",
            "reciever_status": "unread",
            "receiver_id": data.get("reciever"),
        }

        not_valid = validate_new_message(**new_message_data)
        response = None

        if not_valid:
            response = not_valid
        elif not db.check_duplicate_message(
                new_message_data["subject"], new_message_data["subject"],
        ):
            new_message_data["user_id"] = get_current_identity()
            new_message = db.create_message(**new_message_data)

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
        else:

            response = (
                jsonify(
                    {"status": 409, "error": "Message already sent"}
                ),
                409,
            )

        return response

    def get_a_message(self, record_id):
        user_id = get_current_identity()
        results = db.get_message_record(record_id, user_id)
        response = None
        if results and "error" in results:
            response = (
                jsonify({"status": 401, "error": results["error"]}), 401)
        elif results:
            response = jsonify({"status": 200, "data": [results]}), 200
        else:

            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "message record with specified id does not exist"
                    }
                ),
                404,
            )

        return response

    def delete_email(self, inbox_mail_id):
        """ 
        deleting an email from a user's inbox.
        """
        user_id = get_current_identity()
        results = db.get_message_record(inbox_mail_id, user_id)
        delete_inbox = db.delete_inbox_mail(inbox_mail_id, user_id
        )
        response = None
        if results:
            delete_inbox
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "mail": results,
                                "success": "Message successfully deleted"
                            }
                        ],
                    }
                ),
                200,
            )
        else:
            response = (
                jsonify(
                    {"status": 404, "error": "Message with such id does not exist"}
                ),
                404,
            )

        return response

    def fetch_sent_emails(self):
        """
        Returns all users sent messages.
        """
        sender_id = get_current_identity()
        collection = db.get_sent_messages(sender_id)
        response = None

        if collection:
            response = (
                jsonify({
                    "status": 200,
                    "data": collection,
                    "message": "These are your sent messages"
                }), 200)

        else:
            response = (
                jsonify(
                    {"status": 404, "error": "You have not sent any mail yet."
                     }), 404
            )
        return response

    def all_received_emails(self):
        receiver_id = get_current_identity()
        inbox = db.get_all_received_messages(receiver_id)
        response = None

        if inbox:
            response = (
                jsonify({
                    "status": 200,
                    "data": inbox,
                    "message": "These are your inbox messages"
                }), 200)

        else:
            response = (
                jsonify(
                    {"status": 404, "error": "You have not received any mail yet."
                     }), 404
            )
        return response


    

