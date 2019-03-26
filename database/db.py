import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import runtime_mode
import os


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

        except (Exception, psycopg2.Error) as e:
            print(e)
    
    def database_connection(self, database_name):
            """Function for connecting to appropriate database"""
            return psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='bekeplar')

        
    def drop_table(self, table_name):
            """
            Drop tables after tests
            """
            drop = f"DROP TABLE {table_name} CASCADE;"
            self.cursor_database.execute(drop)


if __name__ == '__main__':
    database_name = DatabaseConnection()
