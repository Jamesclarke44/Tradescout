import sqlite3
import pandas as pd
import os

# -----------------------------
# SAFE PATH HANDLING
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "stocks.db")


# -----------------------------
# INIT DATABASE (SAFE STARTUP)
# -----------------------------

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


# -----------------------------
# LOAD DATA FOR STREAMLIT
# -----------------------------

def load_data():
    init_db()  # ensures DB always exists before reading

    conn = sqlite3.connect(DB_PATH)

    scans = pd.read_sql_query("SELECT * FROM scan_results", conn)

    try:
        perf = pd.read_sql_query("SELECT * FROM performance", conn)
    except:
        perf = pd.DataFrame()

    conn.close()

    return scans, perf