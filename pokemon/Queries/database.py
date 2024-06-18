import json
import os

import mysql.connector
from dotenv import load_dotenv

# config_path = os.path.join(os.path.dirname(__file__), '..', 'config.env')
#
# def connect_to_database():
#     with open(config_path, 'r') as f:
#         db_config = json.load(f)
#
#     db_config = db_config['database']
#     print(db_config)
#     return mysql.connector.connect(
#         host=db_config['host'],
#         user=db_config['user'],
#         port=db_config['port'],
#         password=db_config['password'],
#         database=db_config['database']
#     )
load_dotenv('config.env')

def connect_to_database():

        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            port=int(os.getenv('MYSQL_PORT', 3306)),  # Default to 3306 if not set
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )

def close_connection(connection):
    connection.close()


def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows


def execute_and_fetch_query(connection, query, data=None):
    cursor = connection.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return [row[0] for row in result]
