import streamlit as st
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "stocks.db")


def load_data():
    conn = sqlite3.connect(DB_PATH)

    try:
        scans = conn.execute("SELECT * FROM scan_results").fetchall()
    except:
        scans = []

    conn.close()
    return scans


st.title("📊 TradeScout Dashboard")

data = load_data()

st.write("Scan Results")

st.write(data)