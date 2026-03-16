import sqlite3

DATABASE = "database/database.db"

def get_db():
    conn = sqlite3.connect(DATABASE,timeout=10,check_same_thread=False)
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
    CREATE TABLE IF NOT EXISTS favorites(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        UNIQUE(user_id,movie_id)
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

