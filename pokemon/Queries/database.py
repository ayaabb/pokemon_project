import json
import os

import mysql.connector
from dotenv import load_dotenv

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
    if len(result) == 0:
        return result
    if len(result) > 1:
        return [row[0] for row in result]
    return result[0]
