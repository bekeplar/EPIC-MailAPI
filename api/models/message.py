from datetime import date
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.responses import (
    duplicate_subject,
    duplicate_message,
)
user_messages = []
message_id = 1


class Message:
    """class to contain all message objects"""
    def __init__(self, **kwargs):
        global message_id
        self.message_id = message_id
        self.subject = kwargs["subject"]
        self.message = kwargs["message"]
        self.sender_status = kwargs["sender_status"]
        self.receiver_status = "unread"
        self.parent_message_id = kwargs["parent_message_id"]
        self.receiver = kwargs["receiver"]
        self.created_on = date.today()
        message_id += 1


def check_duplicate_message(subject, Message):
    """Testing for uniqueness of a message."""
    for message in user_messages:
        if message['subject'] == subject:
            return duplicate_subject
        elif message['Message'] == message:
            return duplicate_message


def get_message_record(message_id):
    """Method to return a given message by id"""
    result = [
        message for message in user_messages
        if message["message_id"] == message_id
    ]
    return result


def get_inbox_record(message_id):
    """Method to delete a given message from user inbox by id."""
    result = [
        message for message in user_messages
        if message["message_id"] == message_id and message["receiver_status"] == "unread"
            
    ]
    return result
    

def get_sent_messages(sender_status, sender_id):
    """Function which returns all sent messages by a user."""
    result = [
        message for message in user_messages
        if message["sender_status"] == "sent" 
    ]
    return result


def get_all_received_messages(receiver_status, receiver_id):
    """Function for getting all received messages."""
    user_rec = get_current_identity()
    result = [
        message for message in user_messages
        if message["receiver_status"] == "unread" or message["receiver_id"] == user_rec
    ]
    return result