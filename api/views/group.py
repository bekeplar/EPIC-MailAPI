from flask import Blueprint, request
from api.controllers.group import GroupController
from api.utilitiez.auth_token import token_required

group_bp = Blueprint("group", __name__, url_prefix="/api/v1")


group_controller = GroupController()


@group_bp.route("/groups", methods=["POST"])
@token_required
def Form_group():
    data = request.get_json(force=True)
    return group_controller.new_group(data)

