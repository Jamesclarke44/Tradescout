from datetime import datetime
from collectors.market_data import get_data
from scanners.scoring import score_stock
from data.database import init_db, save_scan

TICKERS = ["AAPL", "TSLA", "AMD", "NVDA", "PLTR"]


def run():
    init_db()
    today = datetime.now().strftime("%Y-%m-%d")

    for ticker in TICKERS:
        df = get_data(ticker)

        score = score_stock(df)
        price = df["Close"].iloc[-1]

        save_scan(today, ticker, score, price)

        print(ticker, score)


if __name__ == "__main__":
    run()