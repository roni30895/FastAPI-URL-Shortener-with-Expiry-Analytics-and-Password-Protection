import sqlite3

db_file_path = "URL_shortener.db"
connection = sqlite3.connect(db_file_path, check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_url TEXT NOT NULL UNIQUE,
    creation_timestamp TEXT NOT NULL,
    expiration_timestamp TEXT NOT NULL,
    password_hash TEXT
)
""")

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS analytics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_url TEXT NOT NULL,
        access_timestamp TEXT NOT NULL,
        ip_address TEXT NOT NULL
    )
"""
)

connection.commit()