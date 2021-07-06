from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")
print(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)


class DBConnection:
    def __init__(self):
        db_config = {
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "database": DB_DATABASE,
            "raise_on_warnings": False,
        }
        self.cnx = connect(**db_config)
        self.cur = self.cnx.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # close db connection
        print(self.cur)
        self.cnx.commit()
        self.cur.close()
        self.cnx.close()


add_user = "INSERT IGNORE INTO users (telegram_id, name) VALUES (%s, %s)"


def write_db(query_name, data):
    try:
        with DBConnection() as connection:
            connection.cur.execute(query_name, data)
    except Error as e:
        print(e)
