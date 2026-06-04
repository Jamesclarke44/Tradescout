import sqlite3
import os

DB_PATH = os.path.join("data", "stocks.db")


# -----------------------------
# CONNECTION
# -----------------------------

def connect():
    return sqlite3.connect(DB_PATH)


# -----------------------------
# TABLE CREATION
# -----------------------------

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Stores daily scan results (your scores)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        ticker TEXT,
        score REAL,
        price REAL
    )
    """)

    # Stores future performance after signals
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


# -----------------------------
# SAVE SCAN RESULTS
# -----------------------------

def save_scan_result(date, ticker, score, price):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scan_results (date, ticker, score, price)
    VALUES (?, ?, ?, ?)
    """, (date, ticker, score, price))

    conn.commit()
    conn.close()


# -----------------------------
# SAVE PERFORMANCE RESULTS
# -----------------------------

def update_performance(ticker, scan_date, price_3d, price_5d, price_10d):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO performance (ticker, scan_date, price_3d, price_5d, price_10d)
    VALUES (?, ?, ?, ?, ?)
    """, (ticker, scan_date, price_3d, price_5d, price_10d))

    conn.commit()
    conn.close()