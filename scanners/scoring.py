from scanners.consolidation import detect_consolidation

def score_stock(df):
    latest = df.iloc[-1]

    score = 0

    if latest["Close"] > latest["Close"].rolling(50).mean().iloc[-1]:
        score += 25

    if latest["Close"] > latest["Close"].rolling(200).mean().iloc[-1]:
        score += 25

    if 55 <= latest.get("RSI", 50) <= 70:
        score += 10

    cons = detect_consolidation(df)
    if cons["consolidating"]:
        score += 20

    return score