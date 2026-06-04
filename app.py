import sqlite3
import pandas as pd
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "stocks.db")


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


def load_data():
    init_db()  # 🔥 THIS MUST RUN FIRST

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query("SELECT * FROM scan_results", conn)
    except Exception as e:
        st.error(f"DB error: {e}")
        df = pd.DataFrame()

    conn.close()

    return df