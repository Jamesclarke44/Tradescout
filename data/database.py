import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
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

    conn.commit()
    conn.close()


def save_scan(date, ticker, score, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scan_results (date, ticker, score, price)
    VALUES (?, ?, ?, ?)
    """, (date, ticker, score, price))

    conn.commit()
    conn.close()


def load_scans():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT date, ticker, score, price FROM scan_results")
    rows = cursor.fetchall()

    conn.close()
    return rows