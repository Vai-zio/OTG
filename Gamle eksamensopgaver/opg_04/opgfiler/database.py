from flask import g
import hashlib
import sqlite3

def connect_db():
    # Connects to our specific database
    con = sqlite3.connect('blog.db')
    con.row_factory = sqlite3.Row

    con.set_trace_callback(print) # Print all queries for learning and fun
    return con 


def get_db():
    # Opens a new database connection if there is none yet
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


def hash_password(password):
    # Naive (insecure) hashing of password
    return hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    
def create_tables():

    db = get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    password TEXT
                  );""")


    db.execute("""CREATE TABLE IF NOT EXISTS posts(
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    date TEXT,
                    text TEXT
                  );""")

    db.execute("""CREATE TABLE IF NOT EXISTS comments(
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    post_id TEXT,
                    date TEXT,
                    text TEXT
                  );""")
    db.commit()
