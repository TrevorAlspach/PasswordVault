import db.database as db
import os
from contextlib import closing

conn = db.create_connection(os.getcwd() + "/db/database.sqlite3")


def create_tables():
    with closing(conn):
        with closing(conn.cursor()) as cursor:
            #cursor.execute("execute your sql here")
            pass
