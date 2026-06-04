import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from data.database import create_tables, save_scan_result
# -----------------------------
# CONFIG
# -----------------------------

TICKERS = [
    "MARA", "SOFI", "F", "PLTR", "AAPL",
    "TSLA", "AMD", "NVDA", "AMZN", "GOOGL"
]

LOOKBACK = "6mo"

# -----------------------------
# INDICATORS
# -----------------------------

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def add_indicators(df):
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["RSI"] = calculate_rsi(df)

    df["AvgVolume20"] = df["Volume"].rolling(20).mean()
    df["RelVolume"] = df["Volume"] / df["AvgVolume20"]

    return df


# -----------------------------
# SCORING SYSTEM (VERSION 1)
# -----------------------------

def score_stock(df):
    latest = df.iloc[-1]

    score = 0

    # Trend
    if latest["Close"] > latest["SMA50"]:
        score += 15

    if latest["Close"] > latest["SMA200"]:
        score += 15

    if latest["SMA50"] > latest["SMA200"]:
        score += 15

    # Momentum
    if 55 <= latest["RSI"] <= 70:
        score += 10

    if latest["RelVolume"] > 1.5:
        score += 20

    # Basic breakout proxy (near highs)
    if latest["Close"] >= df["Close"].rolling(52).max().iloc[-1] * 0.97:
        score += 10

    return score


# -----------------------------
# DATA LOADER
# -----------------------------

def get_data(ticker):
    df = yf.download(ticker, period=LOOKBACK, interval="1d", progress=False)
    df.dropna(inplace=True)
    return df


# -----------------------------
# MAIN SCANNER
# -----------------------------

def run_scanner():
    results = []

    for ticker in TICKERS:
        try:
            df = get_data(ticker)
            df = add_indicators(df)

            if len(df) < 200:
                continue

            score = score_stock(df)

            results.append({
                "Ticker": ticker,
                "Score": score,
                "Price": round(df["Close"].iloc[-1], 2)
            })

        except Exception as e:
            print(f"Error with {ticker}: {e}")

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="Score", ascending=False)

    print("\n=== TRADE SCOUT V1 RESULTS ===\n")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    run_scanner()