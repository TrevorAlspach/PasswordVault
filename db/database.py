import sqlite3
from sqlite3 import Error
import os


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to DB successful")
    except Error as e:
        print(f"Error: {e}")

    return conn


if not os.path.isfile('db/database.db'):
    originalPassword = "password"
    conn = sqlite3.connect('db/database.db')
    conn.execute('CREATE TABLE Passwords(Site TEXT(50), Username TEXT(50), Password TEXT(50), DecodeKey TEXT(150))')
    conn.execute('CREATE TABLE Master(password TEXT(150))')
    conn.commit()
    conn.commit()
    conn.close()

