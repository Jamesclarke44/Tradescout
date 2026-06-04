from scanners.consolidation import detect_consolidation

def score_stock(df):
    latest = df.iloc[-1]

    score = 0

    # ---------------- Trend ----------------
    if latest["Close"] > latest["SMA50"]:
        score += 15

    if latest["Close"] > latest["SMA200"]:
        score += 15

    if latest["SMA50"] > latest["SMA200"]:
        score += 15

    # ---------------- Momentum ----------------
    if 55 <= latest["RSI"] <= 70:
        score += 10

    if latest["RelVolume"] > 1.5:
        score += 20

    # ---------------- Breakout proximity ----------------
    high_52w = df["Close"].rolling(252).max().iloc[-1]
    if latest["Close"] >= high_52w * 0.97:
        score += 10

    # ---------------- Consolidation ----------------
    cons = detect_consolidation(df)
    if cons["consolidating"]:
        score += 15

    return score