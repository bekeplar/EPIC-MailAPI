from flask import Blueprint, request
from api.controllers.message import MessagesController
from api.utilitiez.auth_token import token_required

messages_bp = Blueprint("messages", __name__, url_prefix="/api/v1")


message_controller = MessagesController()


@messages_bp.route("/messages", methods=["POST"])
@token_required
def add_email():
    data = request.get_json(force=True)
    return message_controller.new_message(data)