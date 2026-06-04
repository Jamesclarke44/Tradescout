import yfinance as yf
from datetime import datetime, timedelta
from data.database import connect, update_performance


def get_future_price(df, days_ahead):
    try:
        return df["Close"].iloc[days_ahead]
    except:
        return None


def run_performance_tracking():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT ticker, date FROM scan_results")
    rows = cursor.fetchall()

    print("\n=== CALCULATING PERFORMANCE ===\n")

    for ticker, scan_date in rows:
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            df.dropna(inplace=True)

            if len(df) < 15:
                continue

            price_3d = get_future_price(df, 3)
            price_5d = get_future_price(df, 5)
            price_10d = get_future_price(df, 10)

            if price_3d is None or price_5d is None or price_10d is None:
                continue

            update_performance(
                ticker,
                scan_date,
                float(price_3d),
                float(price_5d),
                float(price_10d)
            )

            print(f"{ticker} | {scan_date} → tracked")

        except Exception as e:
            print(f"Error {ticker}: {e}")


if __name__ == "__main__":
    run_performance_tracking()