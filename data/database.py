import sqlite3
import os

DB_PATH = os.path.join("data", "stocks.db")


def connect():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        ticker TEXT,
        score REAL,
        price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT,
        scan_date TEXT,
        price_3d REAL,
        price_5d REAL,
        price_10d REAL
    )
    """)

    conn.commit()
    conn.close()


def save_scan_result(date, ticker, score, price):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scan_results (date, ticker, score, price)
    VALUES (?, ?, ?, ?)
    """, (date, ticker, score, price))

    conn.commit()
    conn.close()