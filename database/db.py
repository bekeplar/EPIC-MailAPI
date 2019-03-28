import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import runtime_mode
import os
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.responses import (
    duplicate_subject,
    duplicate_message,
    duplicate_group,
    duplicate_member,
)
from api.utilitiez.responses import (
    duplicate_email,
)


class DatabaseConnection:
    def __init__(self):
        """class initializing method"""
        try:
            self.database_name = ""
            self.database_connect = None

            if runtime_mode == "Development":
                self.database_connect = self.database_connection("postgres")

            if runtime_mode == "Testing":
                self.database_connect = self.database_connection("testing_db")

            if runtime_mode == "Production":
                DATABASE_URL = os.environ['DATABASE_URL']
                self.database_connect = psycopg2.connect(DATABASE_URL, sslmode='require')

            self.database_connect.autocommit = True
            self.cursor_database = self.database_connect.cursor(cursor_factory=RealDictCursor)
            print('Connected to the database successfully.')
            
            create_user_table = """CREATE TABLE IF NOT EXISTS users
            (
                user_id SERIAL NOT NULL PRIMARY KEY,
                first_name VARCHAR(25) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                user_password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                is_admin BOOLEAN DEFAULT FALSE
            );"""

            create_message_table = """CREATE TABLE IF NOT EXISTS messages
            (
                message_id SERIAL NOT NULL PRIMARY KEY,
                subject VARCHAR(125) NOT NULL,
                message TEXT NOT NULL,
                sender_status VARCHAR(50) NOT NULL,
                receiver_status VARCHAR(50) NOT NULL,
                parent_message_id INT NOT NULL,
                created_on  DATE DEFAULT CURRENT_TIMESTAMP,
                sender_id VARCHAR(50) NOT NULL,
                receiver_id INT NOT NULL
            );"""

            create_group_table = """CREATE TABLE IF NOT EXISTS groups
            (
                group_id SERIAL NOT NULL PRIMARY KEY,
                group_name VARCHAR(25) NOT NULL,
                is_admin BOOLEAN DEFAULT TRUE
            );"""


            create_group_members_table = """CREATE TABLE IF NOT EXISTS group_members
            (
                group_id SERIAL NOT NULL PRIMARY KEY,
                user_id INT NOT NULL REFERENCES users(user_id),
                is_admin BOOLEAN DEFAULT FALSE
            );"""

            create_auth_table = """CREATE TABLE IF NOT EXISTS users_auth
            (
                user_id SERIAL NOT NULL PRIMARY KEY,
                token VARCHAR(255) NOT NULL,
                is_blacklisted BOOLEAN DEFAULT FALSE,
                last_login DATE DEFAULT CURRENT_TIMESTAMP
            );"""
            self.cursor_database.execute(create_user_table)
            self.cursor_database.execute(create_message_table)
            self.cursor_database.execute(create_group_table)
            self.cursor_database.execute(create_auth_table)
            self.cursor_database.execute(create_group_members_table)
        except (Exception, psycopg2.Error) as e:
            print(e)
    
    def database_connection(self, database_name):
            """Function for connecting to appropriate database"""
            return psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='bekeplar')

    
    def insert_user(self, **kwargs):
        """User class method for adding new user to the users database"""
        first_name = kwargs["first_name"]
        last_name = kwargs["last_name"]
        email = kwargs["email"]
        user_password = generate_password_hash(kwargs["password"])
        # Querry for adding a new user into users_db
        sql = (
            "INSERT INTO users ("
            "first_name,"
            "last_name, "
            "email,"
            "user_password )VALUES ("
            f"'{first_name}', '{last_name}','{email}',"
            f"'{user_password}') returning "
            "user_id, first_name as firstname,"
            "last_name as lastname,"
            "email as email"
        )
        self.cursor_database.execute(sql)
        new_user = self.cursor_database.fetchone()
        return new_user

    def check_if_user_exists(self, email):
        """Making sure that a user's email is unique"""
        user_exists_sql = (
            "SELECT email from users where "
            f" email='{email}';"
        )
        self.cursor_database.execute(user_exists_sql)
        user_exists = self.cursor_database.fetchone()
        error = {}

        if user_exists and user_exists.get("email") == email:
            error["email"] = duplicate_email

        return error

    def is_valid_credentials(self, email, user_password):
        """Function for verrifying user credentials before login"""
        sql = (
            "SELECT user_id, email ,user_password FROM users \
                where email="
            f"'{email}';"
        )
        self.cursor_database.execute(sql)

        user_details = self.cursor_database.fetchone()

        if (
                user_details
                and user_details.get("email") == email
                and check_password_hash(
                user_details.get("user_password"), user_password
        )
        ):
            id = user_details.get("user_id")

            return id
        return None
    
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
        self.cursor_database.execute(sql)
        new_incident = self.cursor_database.fetchone()
        return new_incident


    def check_duplicate_message(self, subject, message):
        """Testing for uniqueness of a message."""
        exists_query = (
            "SELECT subject, Message from messages where "
            f"subject ='{subject}' OR message='{message}';"
        )
        self.cursor_database.execute(exists_query)
        message_exists = self.cursor_database.fetchone()
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
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def get_inbox_record(self, owner_id, msg_id):
        """Method to delete a given message from user inbox by id."""
        sql = (
            f"SELECT * FROM messages WHERE receiver_id='{owner_id}' \
                    AND message_id='{msg_id}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def get_sent_messages(self, owner_id):
        """Function which returns all sent messages by a user."""
        sql = (
            f"SELECT * FROM messages WHERE sender_id='{owner_id}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def get_all_received_messages(self, owner_id):
        """Function for getting all received messages."""
        sql = (
            f"SELECT * FROM messages WHERE receiver_id='{owner_id}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def delete_inbox_mail(self, msg_id, user_id):
        """Function to delete a user's inbox mail."""
        sql = (
            f"DELETE FROM messages WHERE receiver_id='{user_id}' "
            f"AND message_id='{msg_id}' returning *;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def insert_new_group(self, **kwargs):
        """A method for adding a new group to the database"""
        group_name = kwargs["group_name"]

        # Querry for adding a new group into the groups database
        sql = (
            "INSERT INTO groups ("
            "group_name)VALUES ("
            f"'{group_name}') returning "
            "group_id, group_name as groupname,"
            "is_admin as is_admin"
        )
        self.cursor_database.execute(sql)
        new_user = self.cursor_database.fetchone()
        return new_user


    def check_duplicate_group(self, group_name):
        """Testing for uniqueness of my created group."""
        exists_query = (
            "SELECT group_name from groups where "
            f"group_name ='{group_name}';"
        )
        self.cursor_database.execute(exists_query)
        group_exists = self.cursor_database.fetchone()
        error = {}
        if group_exists and group_exists.get("group_name") == group_name:
            error["group_name"] = duplicate_group
        return error


    def delete_group(self, grp_id):
        """Function for deleting a group."""
        sql = (
            f"DELETE FROM groups WHERE group_id='{grp_id}' returning*;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def get_group_record(self, grp_id):
        """Function for fetching a specific group ny its id."""
        sql = (
            f"SELECT * FROM groups WHERE group_id='{grp_id}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def get_all_groups(self):
        """Method to all groups"""
        sql = (
            f"SELECT * FROM groups;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchall()


    def update_group_name(self, grp_id, grp_name):
        """Method for updating a user's group name."""
        sql = (
            f"UPDATE groups SET group_name='{grp_name}' "
            f"WHERE group_id='{grp_id}' returning group_id , group_name;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()


    def drop_table(self, table_name):
            """
            Drop tables after tests
            """
            drop = f"DROP TABLE {table_name} CASCADE;"
            self.cursor_database.execute(drop)


if __name__ == '__main__':
    database_name = DatabaseConnection()
