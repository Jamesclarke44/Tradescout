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


def save_scan(date, ticker, score, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scan_results (date, ticker, score, price)
    VALUES (?, ?, ?, ?)
    """, (date, ticker, score, price))

    conn.commit()
    conn.close()


def load_data():
    init_db()

    conn = sqlite3.connect(DB_PATH)

    scans = conn.execute("SELECT * FROM scan_results").fetchall()

    try:
        perf = conn.execute("SELECT * FROM performance").fetchall()
    except:
        perf = []

    conn.close()

    return scans, perf