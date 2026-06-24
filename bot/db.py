from mysql.connector import connect, Error
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv('../.env')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')


def log(msg):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}')


log('Env loaded.')


class DBConnection:
    def __init__(self):
        db_config = {
            'user': DB_USER,
            'password': DB_PASSWORD,
            'host': DB_HOST,
            'database': DB_DATABASE,
            'raise_on_warnings': False,
        }
        self.cnx = connect(**db_config)
        self.cur = self.cnx.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.commit()
        self.cur.close()
        self.cnx.close()


def query_db(query_name, data):
    try:
        with DBConnection() as connection:
            connection.cur.execute(query_name, data)
            if query_name.strip().upper().startswith('SELECT'):
                return connection.cur.fetchall()
            return None
    except Error as e:
        log(f'DB Error: {e}')
        return None
