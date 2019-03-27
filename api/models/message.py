from datetime import date

class Message:
    """class to contain all message objects"""

    def __init__(self, **kwargs):
        self.message_id =kwargs["message_id"]
        self.subject = kwargs["subject"]
        self.message = kwargs["message"]
        self.sender_status = kwargs["sender_status"]
        self.receiver_status = "unread"
        self.parent_message_id = kwargs["parent_message_id"]
        self.sender_id = kwargs["sender_id"]
        self.receiver_id = kwargs["receiver_id"]
        self.created_on = date.today()
