# db.py
import sqlite3
from datetime import datetime

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("database.db")  # creates file if not exists
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recognition_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a new log entry
def log_recognition(name, source):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO recognition_log (name, source, timestamp)
        VALUES (?, ?, ?)
    """, (name, source, timestamp))
    conn.commit()
    conn.close()
