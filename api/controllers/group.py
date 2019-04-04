from flask import Blueprint, jsonify, json, request
from api.models.group import Group
from database.db import DatabaseConnection
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.validation import validate_group, validate_name

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
                                "group": created_group,
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


    def delete_one_group(self, group_id):
        """ 
        Logic for deleting a group.
        """
        results = db.get_group_record(group_id)
        remove_group = db.delete_group(group_id)

        response = None
        if results:
            remove_group
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "groups": results,
                                "success": "Group successfully deleted"
                            }
                        ],
                    }
                ),
                200,
            )
        else:
            response = (
                jsonify(
                    {"status": 404, "error": "Group with such id does not exist"}
                ),
                404,
            )

        return response

    def fetch_groups(self):
        """ 
        Logic for getting all groups.
        """
        results = db.get_all_groups()
        response = None
        if results:
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": results,
                        "success": "The following are your groups"
                    }
                ),
                200,
            )
        else:
            response = (
                jsonify(
                    {"status": 404, "error": "You dont have any group created yet"}
                ),
                404,
            )
        return response



    def edit_group_name(self, group_id, data):
        """Function for changing the name of a group"""
        group_name = request.get_json(force=True).get("new_name")
        identity = db.get_group_record(group_id)
        response = None
        if not identity:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "Group record with specified id does not exist",
                    }
                ),
                404,
            )
        else:
            results = db.update_group_name(group_id, group_name)
            is_admin = True
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "id": results["group_id"],
                                "name": results["group_name"],
                                "is_admin": is_admin,
                                "success": "Group name updated successfully",
                            }
                        ],
                    }
                ),
                200,
            )
        return response