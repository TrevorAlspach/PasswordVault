import sqlite3
from sqlite3 import Error


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to DB successful")
    except Error as e:
        print(f"Error: {e}")

    return conn
