import sqlite3
import pandas as pd

DB_PATH = "data/stocks.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)

    scans = pd.read_sql_query("SELECT * FROM scan_results", conn)
    perf = pd.read_sql_query("SELECT * FROM performance", conn)

    conn.close()

    return scans, perf


def build_edge_report():
    scans, perf = load_data()

    if scans.empty or perf.empty:
        print("Not enough data yet.")
        return

    # Rename for merge
    scans = scans.rename(columns={"date": "scan_date"})

    merged = pd.merge(
        scans,
        perf,
        on=["ticker", "scan_date"],
        how="inner"
    )

    # -----------------------------
    # Calculate returns
    # -----------------------------

    merged["ret_3d"] = (merged["price_3d"] - merged["price"]) / merged["price"] * 100
    merged["ret_5d"] = (merged["price_5d"] - merged["price"]) / merged["price"] * 100
    merged["ret_10d"] = (merged["price_10d"] - merged["price"]) / merged["price"] * 100

    # -----------------------------
    # Score buckets
    # -----------------------------

    def bucket(score):
        if score >= 90:
            return "90-100"
        elif score >= 80:
            return "80-89"
        elif score >= 70:
            return "70-79"
        else:
            return "<70"

    merged["bucket"] = merged["score"].apply(bucket)

    # -----------------------------
    # Group analysis
    # -----------------------------

    report = merged.groupby("bucket")[["ret_3d", "ret_5d", "ret_10d"]].mean()

    print("\n=== EDGE REPORT ===\n")
    print(report)

    # Optional: sample size per bucket
    counts = merged["bucket"].value_counts()

    print("\n=== SAMPLE SIZE ===\n")
    print(counts)


if __name__ == "__main__":
    build_edge_report()