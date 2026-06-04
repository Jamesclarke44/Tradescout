import yfinance as yf

def get_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d", progress=False)
    df.dropna(inplace=True)
    return df