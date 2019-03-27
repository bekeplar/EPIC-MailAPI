from flask import Blueprint, jsonify, json, request
from api.models.group import Group
from database.db import DatabaseConnection
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.validation import validate_group

db = DatabaseConnection()


class GroupController():

    def new_group(self, data):
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

        group_data = {
            "group_name": data.get("group_name"),
        }

        not_valid = validate_group(**group_data)
        response = None

        if not_valid:
            response = not_valid
        elif not db.check_duplicate_group(
                group_data["group_name"],
        ):
            created_group = db.insert_new_group(**group_data)

            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "mail": created_group,
                                "message": "Group created successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        else:

            response = (
                jsonify(
                    {"status": 409, "error": "The group already exists"}
                ),
                409,
            )

        return response