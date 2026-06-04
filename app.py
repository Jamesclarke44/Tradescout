import streamlit as st
from datetime import datetime

from main import run   # your scanner function
import sqlite3
import os
import pandas as pd

st.title("📊 TradeScout Dashboard")

if st.button("🚀 Run Scanner Now"):
    run()
    st.success("Scan complete!")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "stocks.db")


def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("SELECT * FROM scan_results", conn)

    conn.close()
    return df


st.title("📊 TradeScout Dashboard")

df = load_data()

if df.empty:
    st.warning("No scan data yet. Run main.py first.")
else:
    df = df.sort_values("score", ascending=False)

    st.subheader("Scan Results")
    st.dataframe(df, use_container_width=True)