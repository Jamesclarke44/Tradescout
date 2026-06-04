def detect_consolidation(df):
    recent = df.tail(10)

    high = recent["High"].max()
    low = recent["Low"].min()

    range_pct = (high - low) / low * 100

    return {
        "consolidating": range_pct < 8,
        "range_pct": range_pct
    }