import sqlite3
from datetime import datetime

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("blog.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def get_db_likes():
    if 'db' not in g:
        g.db = sqlite3.connect("likes.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def get_db_follows():
    if 'db' not in g:
        g.db = sqlite3.connect("follows.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_db():
    con = get_db()
    sql = """CREATE TABLE IF NOT EXISTS posts (
                 userid INTEGER PRIMARY KEY,
                 name TEXT,
                 title TEXT,
                 date TEXT,
                 body TEXT
            ); 
             """
    con.execute(sql)
    con.commit()

def create_db():
    con = get_db()
    sql = """CREATE TABLE IF NOT EXISTS likes (
                 id INTEGER PRIMARY KEY,
                 postid TEXT,
                 userid INTEGER,
                 date TEXT
            ); 
             """
    con.execute(sql)
    con.commit()

def create_db():
    con = get_db()
    sql = """CREATE TABLE IF NOT EXISTS follows (
                 userid INTEGER PRIMARY KEY,
                 followid TEXT,
                 upvotes TEXT,
                 date TEXT
            ); 
             """
    con.execute(sql)
    con.commit()