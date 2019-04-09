from flask import Flask, jsonify, Blueprint
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

    @app.route("/")
    def _home():
        return (
            jsonify({"message": "Welcome to Epic-Email App", "status": 200}),
            200,
        )

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