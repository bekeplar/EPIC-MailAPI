from api.utilitiez.validation import sign_up_data_required
from flask import Blueprint
from api.controllers.auth import UserController

users_bp = Blueprint("users", __name__, url_prefix="/api/v2")


user_controller = UserController()


@users_bp.route("/auth/signup", methods=["POST"])
@sign_up_data_required
def register_user():
    return user_controller.signup()


@users_bp.route("/auth/login", methods=["POST"])
def login_user():
    return user_controller.login()
