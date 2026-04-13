import psycopg
from flask import g, current_app
from psycopg.rows import dict_row


def get_db():
    if "db" not in g:
        g.db = psycopg.connect(
            current_app.config["DATABASE_URL"],
            connect_timeout=10,
        )
        g.db.row_factory = dict_row
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        conn = psycopg.connect(app.config["DATABASE_URL"])
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites(
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_id INTEGER,
            movie_id INTEGER,
            UNIQUE(user_id, movie_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments(
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            movie_id INTEGER,
            user_name TEXT,
            anonymous INTEGER,
            contents TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()
