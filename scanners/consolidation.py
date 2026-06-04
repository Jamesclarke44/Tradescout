import numpy as np

def detect_consolidation(df, lookback=10):
    """
    Detects if price is in a tight consolidation range.
    Returns score (0 or 1) and range width.
    """

    recent = df.tail(lookback)

    high = recent["High"].max()
    low = recent["Low"].min()

    range_pct = (high - low) / low * 100

    # Tight range = potential breakout setup
    is_consolidating = range_pct < 8  # adjustable threshold

    return {
        "consolidating": is_consolidating,
        "range_pct": range_pct
    }