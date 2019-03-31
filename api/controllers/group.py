from flask import Blueprint, jsonify, json, request
from api.models.group import Group
from database.db import DatabaseConnection
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.validation import (
    validate_group,
    validate_name, 
    validate_new_message,
    )

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
                        "data": [
                            {
                                "groups": results,
                                "success": "The following are your groups"
                            }
                        ],
                    }
                ),
                200,
            )
        else:
            response = (
                jsonify(
                    {"status": 404, 
                    "error": "You dont have any group created yet"}
                ),
                404,
            )
        return response


    def edit_group_name(self, group_id, data):
        """Function for changing the name of a group"""
        group_name = request.get_json(force=True).get("group_name")
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
                                "id": results,
                                "is_admin": is_admin,
                                "success": "Group name updated successfully",
                            }
                        ],
                    }
                ),
                200,
            )
        return response
    

    def add_member(self, data):
        if not request.data:
            return (
                jsonify(
                    {
                        "error": "Please select member to add",
                        "status": 400,
                    }
                ),
                400,
            )
        data = request.get_json(force=True)
        member_data = {
            "user_id": data.get("user_id"),
        }
        if not db.check_member_exists(
                member_data["user_id"],
        ):
            new_member = db.create_new_group_member(**member_data)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "member": new_member,
                                "message": "member added successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        else:

            response = (
                jsonify(
                    {"status": 409, "error": "This member already exists"}
                ),
                409,
            )

        return response


    def remove_member(self, user_id, group_id):
        """ 
        Logic for deleting a group member.
        """
        results = db.get_member(user_id)
        blacklist_member = db.delete_group_member(user_id, group_id)
        response = None
        if results:
            blacklist_member
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "groups": results,
                                "success": "member successfully deleted"
                            }
                        ],
                    }
                ),
                200,
            )
        else:
            response = (
                jsonify(
                    {"status": 404, 
                    "error": "No member with specified id exists"}
                ),
                404,
            )
        return response


    def new_group_message(self, data):
        if not request.data:
            return (
                jsonify(
                    {
                        "error": "Please provide some data",
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
            "group_id": data.get("groupId"),
        }

        not_valid = validate_new_message(**new_message_data)
        group_exist = db.get_user(data.get("groupId"))
        response = None
        if not group_exist:
            response = (
                jsonify(
                    {"status": 404, "error": "Group does not exist."}
                ),
                404,
            )  
        if not_valid:
            response = not_valid
            new_message_data["user_id"] = get_current_identity()
            new_message = db.create_group_message(**new_message_data)

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
                    {"status": 404,
                     "error": "You are not a member to that group."}
                ),
                404,
            )
        return response

