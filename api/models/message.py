from datetime import date
from api.utilitiez.auth_token import get_current_identity
from database.db import DatabaseConnection
from api.utilitiez.responses import (
    duplicate_subject,
    duplicate_message,
)


class Message:
    """class to contain all message objects"""

    def __init__(self):
        self.db = DatabaseConnection()

    def create_message(self, **kwargs):
        """Function for adding a new message to the database"""
        subject = kwargs.get("subject")
        message = kwargs.get("message")
        sender_status = "sent"
        receiver_status = "unread"
        receiver_id = kwargs.get("receiver_id")
        sender_id = kwargs.get("user_id")
        parent_message_id = kwargs.get("parent_message_id")
        created_on = date.today()

        # sql command for inserting a new message in the database
        sql = (
            "INSERT INTO messages ("
            "subject, message, sender_status, receiver_status, receiver_id, sender_id, parent_message_id, created_on"
            ")VALUES ("
            f"'{subject}', '{message}','{sender_status}', '{receiver_status}',"
            f"'{sender_id}', '{receiver_id}', '{parent_message_id}' ,'{created_on}') returning "
            "message_id,subject as subject,"
            "message as message, "
            "sender_status as sender_status,"
            "receiver_status as receiver_status, "
            "receiver_id as receiver_id, "
            "parent_message_id as parent_message_id, "
            "created_on as created_on, "
            "sender_id as sender_id;"
        )
        self.db.cursor_database.execute(sql)
        new_incident = self.db.cursor_database.fetchone()
        return new_incident


    def check_duplicate_message(self, subject, message):
        """Testing for uniqueness of a message."""
        exists_query = (
            "SELECT subject, Message from messages where "
            f"subject ='{subject}' OR message='{message}';"
        )
        self.db.cursor_database.execute(exists_query)
        message_exists = self.db.cursor_database.fetchone()
        error = {}
        if message_exists and message_exists.get("subject") == subject:
            error["subject"] = duplicate_subject

        if message_exists and message_exists.get("message") == message:
            error["message"] = duplicate_message
        return error


    def get_message_record(self, msg_id, owner_id):
        """Method to return a given message by id"""
        sql = (
            f"SELECT * FROM messages WHERE message_id='{msg_id}' \
                    AND receiver_id='{owner_id}';"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()


    def get_inbox_record(self, owner_id, msg_id):
        """Method to delete a given message from user inbox by id."""
        sql = (
            f"SELECT * FROM messages WHERE receiver_id='{owner_id}' \
                    AND message_id='{msg_id}';"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()


    def get_sent_messages(self, owner_id):
        """Function which returns all sent messages by a user."""
        sql = (
            f"SELECT * FROM messages WHERE sender_id='{owner_id}';"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()


    def get_all_received_messages(self, owner_id):
        """Function for getting all received messages."""
        sql = (
            f"SELECT * FROM messages WHERE receiver_id='{owner_id}';"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()


    def delete_inbox_mail(self, msg_id, user_id):
        """Function to delete a user's inbox mail."""
        sql = (
            f"DELETE FROM messages WHERE receiver_id='{user_id}' "
            f"AND message_id='{msg_id}' returning *;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()


