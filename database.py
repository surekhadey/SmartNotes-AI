import sqlite3
from datetime import datetime


DATABASE_NAME = "notes.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            score INTEGER,
            total INTEGER,
            date TEXT
        )
    """)

    connection.commit()

    connection.close()


def save_document(filename):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents (filename, upload_date)
        VALUES (?, ?)
        """,
        (filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    connection.commit()

    connection.close()


def save_quiz_result(filename, score, total):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_results
        (filename, score, total, date)
        VALUES (?, ?, ?, ?)
        """,
        (
            filename,
            score,
            total,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    connection.commit()

    connection.close()