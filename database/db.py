import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import runtime_mode
import os
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.responses import (
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
                self.database_connect = psycopg2.connect(
                    DATABASE_URL, sslmode='require')

            self.database_connect.autocommit = True
            self.cursor_database = self.database_connect.cursor(
                cursor_factory=RealDictCursor)
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
                parent_message_id INT DEFAULT 0,
                created_on  DATE DEFAULT CURRENT_TIMESTAMP,
                sender TEXT NOT NULL,
                reciever TEXT NOT NULL
            );"""

            create_group_messages_table = """CREATE TABLE IF NOT EXISTS group_messages
            (
                message_id SERIAL NOT NULL PRIMARY KEY,
                subject VARCHAR(125) NOT NULL,
                message TEXT NOT NULL,
                sender_status VARCHAR(50) NOT NULL,
                receiver_status VARCHAR(50) NOT NULL,
                parent_message_id INT DEFAULT 0,
                created_on  DATE DEFAULT CURRENT_TIMESTAMP,
                sender TEXT NOT NULL,
                group_id INT NOT NULL
            );"""

            create_group_table = """CREATE TABLE IF NOT EXISTS groups
            (
                group_id SERIAL NOT NULL PRIMARY KEY,
                group_name VARCHAR(25) NOT NULL,
                created_by TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT TRUE
            );"""

            create_group_members_table = """CREATE TABLE IF NOT EXISTS group_members
            (
                group_id SERIAL NOT NULL PRIMARY KEY,
                user_id INT NOT NULL,
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
            self.cursor_database.execute(create_group_messages_table)
        except (Exception, psycopg2.Error) as e:
            print(e)

    def database_connection(self, database_name):
        """Function for connecting to appropriate database"""
        return psycopg2.connect(dbname='postgres', user='postgres',
        host='localhost', password='bekeplar')


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
            email=user_details.get("email")

            return {"id":id, 'email':email}
        return None

    def create_message(self, **kwargs):
        """Function for adding a new group message to the database"""
        subject = kwargs.get("subject")
        message = kwargs.get("message")
        sender_status = "sent"
        receiver_status = "unread"
        reciever = kwargs.get("reciever")
        sender = kwargs.get("user_id")
        created_on = date.today()

        # sql command for inserting a new message in the database
        sql = (
            "INSERT INTO messages ("
            "subject, message, sender_status, receiver_status, reciever, sender, created_on"
            ")VALUES ("
            f"'{subject}', '{message}','{sender_status}', '{receiver_status}',"
            f"'{reciever}', '{sender}' ,'{created_on}') returning "
            "message_id,subject as subject,"
            "message as message, "
            "sender_status as sender_status,"
            "receiver_status as receiver_status, "
            "sender as sender, "
            "parent_message_id as parent_message_id, "
            "created_on as created_on, "
            "reciever as reciever;"
        )
        self.cursor_database.execute(sql)
        new_message = self.cursor_database.fetchone()
        return new_message

    def create_group_message(self, **kwargs):
        """Function for adding a new group message to the database"""
        subject = kwargs.get("subject")
        message = kwargs.get("message")
        sender_status = "sent"
        receiver_status = "unread"
        group_id = kwargs.get("groupId")
        sender = kwargs.get("user_id")
        created_on = date.today()

        # sql command for inserting a new message in the database
        sql = (
            "INSERT INTO group_messages ("
            "subject, message, sender_status, receiver_status, group_id, sender, created_on"
            ")VALUES ("
            f"'{subject}', '{message}','{sender_status}', '{receiver_status}',"
            f"'{group_id}', '{sender}', '{created_on}') returning "
            "message_id,subject as subject,"
            "message as message, "
            "sender_status as sender_status,"
            "receiver_status as receiver_status, "
            "sender as sender, "
            "parent_message_id as parent_message_id, "
            "created_on as created_on, "
            "group_id as group_id;"
        )
        self.cursor_database.execute(sql)
        new_message = self.cursor_database.fetchone()
        return new_message

    def get_message_record(self, msg_id, owner):
        """Method to return a given message by id"""
        sql = (
            f"SELECT * FROM messages WHERE message_id='{msg_id}' \
                    AND reciever='{owner}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()

    def get_inbox_record(self, owner, msg_id):
        """Method to delete a given message from user inbox by id."""
        sql = (
            f"SELECT * FROM messages WHERE reciever='{owner}' \
                    AND message_id='{msg_id}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()

    def get_sent_messages(self, owner):
        """Function which returns all sent messages by a user."""
        sql = (
            f"SELECT * FROM messages WHERE sender='{owner}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchall()

    def get_all_received_messages(self, owner):
        """Function for getting all received messages."""
        sql = (
            f"SELECT * FROM messages WHERE reciever='{owner}';"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchall()

    def get_user(self, owner):
        """Function for checking for an existing user."""
        sql = (
            f"SELECT email FROM users WHERE email='{owner}';"
        )
        self.cursor_database.execute(sql)
        user_in_db = self.cursor_database.fetchone()
        return user_in_db if True else False

    def get_group(self, grp_id):
        """Function for checking for an existing group."""
        sql = (
            f"SELECT group_id FROM groups WHERE group_id='{grp_id}';"
        )
        self.cursor_database.execute(sql)
        group_in_db = self.cursor_database.fetchone()
        return group_in_db if True else False

    def get_group_member(self, sender):
        """Function for checking for an existing group member."""
        sql = (
            f"SELECT group_id FROM group_members WHERE user_id='{sender}';"
        )
        self.cursor_database.execute(sql)
        member_in_grp = self.cursor_database.fetchone()
        return member_in_grp if True else False


    def delete_inbox_mail(self, msg_id, user):
        """Function to delete a user's inbox mail."""
        sql = (
            f"DELETE FROM messages WHERE reciever='{user}' "
            f"AND message_id='{msg_id}' returning *;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()

    def insert_new_group(self, **kwargs):
        """A method for adding a new group to the database"""
        group_name = kwargs["group_name"]
        created_by = kwargs["user_id"]

        # Querry for adding a new group into the groups database
        sql = (
            "INSERT INTO groups ("
            "group_name,"
            "created_by)VALUES ("
            f"'{group_name}', '{created_by}') returning "
            "group_id, created_by as created_by," 
            "group_name as groupname,"
            "is_admin as is_admin"
        )
        self.cursor_database.execute(sql)
        new_group = self.cursor_database.fetchone()
        return new_group

    def create_new_group_member(self, **kwargs):
        """A method for adding a new group member to members database"""
        user_id = kwargs["user_id"]
        # Querry for adding a new group member.
        sql = (
            "INSERT INTO group_members ("
            "user_id)VALUES ("
            f"'{user_id}') returning "
            "group_id, user_id as user_id,"
            "is_admin as is_admin"
        )
        self.cursor_database.execute(sql)
        new_member = self.cursor_database.fetchone()
        return new_member

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

    def check_member_exists(self, member):
        """Testing for uniqueness of a group memeber"""
        exists_query = (
            "SELECT * from group_members where "
            f"user_id ='{member}';"
        )
        self.cursor_database.execute(exists_query)
        member_exists = self.cursor_database.fetchone()
        error = {}
        if member_exists and member_exists.get("user_id") == member:
            error["user_id"] = "Member already added"
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

    def get_all_groups(self, owner):
        """Method to all groups"""
        sql = (
            f"SELECT * FROM groups WHERE created_by='{owner}' ;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchall()

    def update_group_name(self, grp_id, grp_name, owner):
        """Method for updating a user's group name."""
        sql = (
            f"UPDATE groups SET group_name='{grp_name}' "
            f"WHERE group_id='{grp_id}'"
            f"AND created_by='{owner}' "
            "returning *;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchall()

    def delete_group_member(self, mbr_id, grp_id):
        """Function for deleting a group member record."""
        sql = (
            f"DELETE FROM group_members WHERE user_id='{mbr_id}' "
            f"AND group_id='{grp_id}' returning *;"
        )
        self.cursor_database.execute(sql)
        return self.cursor_database.fetchone()

    def get_member(self, mbr_id):
        sql = (
            f"SELECT * FROM group_members WHERE user_id='{mbr_id}';"
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
