from flask import Blueprint, request
from api.controllers.group import GroupController
from api.utilitiez.auth_token import token_required

group_bp = Blueprint("group", __name__, url_prefix="/api/v2")


group_controller = GroupController()


@group_bp.route("/groups", methods=["POST"])
@token_required
def Form_group():
    data = request.get_json()
    return group_controller.new_group(data)


@group_bp.route("/groups/<group_id>", methods=["DELETE"])
@token_required
def get_group_deleted(group_id):
    return group_controller.delete_one_group(group_id)


@group_bp.route("/groups", methods=["GET"])
@token_required
def All_group():
    return group_controller.fetch_groups()


@group_bp.route("/groups/<group_id>/name", methods=["PATCH"])
@token_required
def new_group_name(group_id):
    data = request.get_json()
    return group_controller.edit_group_name(group_id, data)


@group_bp.route("/groups/<group_id>/users", methods=["POST"])
@token_required
def new_group_add(group_id):
    data = request.get_json()
    return group_controller.add_member(data)


@group_bp.route("/groups/<group_id>/users/<user_id>", methods=["DELETE"])
@token_required
def destroy_user(user_id, group_id):
    return group_controller.remove_member(user_id, group_id)



