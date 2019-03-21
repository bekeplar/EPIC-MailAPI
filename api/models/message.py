from datetime import date
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
        self.parent_message_id = kwargs["parent_message_id"]
        self.created_on = date.today()
        self.status = "draft"
        message_id += 1


def check_duplicate_message(subject, Message):
    """Testing for uniqueness of a message"""
    for message in user_messages:
        if message['subject'] == subject:
            return duplicate_subject
        elif message['Message'] == message:
            return duplicate_message
