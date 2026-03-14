import sqlite3

DATABASE = "database/database.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_user(username,password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username,password)
    )

    conn.commit()
    conn.close()

