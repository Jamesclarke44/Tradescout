import streamlit as st
import sqlite3
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

DB_PATH = "data/stocks.db"


# -----------------------------
# LOAD DATA
# -----------------------------

def load_data():
    conn = sqlite3.connect(DB_PATH)

    scans = pd.read_sql_query("SELECT * FROM scan_results", conn)

    try:
        perf = pd.read_sql_query("SELECT * FROM performance", conn)
    except:
        perf = pd.DataFrame()

    conn.close()
    return scans, perf


# -----------------------------
# APP
# -----------------------------

st.set_page_config(page_title="TradeScout Dashboard", layout="wide")

st.title("📊 TradeScout Research Dashboard")

scans, perf = load_data()

# -----------------------------
# RAW SCANS
# -----------------------------

st.header("Latest Scan Results")

if not scans.empty:
    scans_sorted = scans.sort_values("score", ascending=False)
    st.dataframe(scans_sorted, use_container_width=True)
else:
    st.write("No scan data yet.")

# -----------------------------
# EDGE ANALYSIS (if available)
# -----------------------------

st.header("Performance Data")

if not perf.empty:
    st.dataframe(perf, use_container_width=True)
else:
    st.write("No performance data yet. Run edge_report first.")

# -----------------------------
# SIMPLE SUMMARY
# -----------------------------

if not scans.empty:
    st.header("Score Distribution")

    st.bar_chart(scans["score"])