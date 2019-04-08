from flask import Flask, jsonify, Blueprint, render_template
from api.views.user import users_bp
from instance.config import app_config
from api.views.message import messages_bp
from api.views.group import group_bp
from flask_cors import CORS


def create_app(config_name):
    
    """Set up Flask application in function in relation to config"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(users_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(group_bp)
    CORS(app)

    @app.route("/", methods=["GET"])
    def _home():
        return render_template("index.html")

    @app.route("/signup.html", methods=["GET"])
    def signup():
        return render_template("signup.html")

    @app.route("/components/user_dashboard.html", methods=["GET"])
    def messages():
        return render_template("./components/user_dashboard.html")

    @app.route("/components/group.html", methods=["GET"])
    def groups():
        return render_template("./components/group.html")

    @app.route("/components/Admin.html", methods=["GET"])
    def members():
        return render_template("./components/Admin.html")


    @app.errorhandler(400)
    def _bad_request(e):
        return (jsonify({"error": "Bad JSON format data", "status": 400}), 400)

    @app.errorhandler(404)
    def _page_not_found(e):
        return (
            jsonify({"error": "Endpoint for specified URL does not exist"}),
            404,
        )

    @app.errorhandler(405)
    def _method_not_allowed(e):
        return (jsonify({"error": "Method not allowed"}), 405)

    return app