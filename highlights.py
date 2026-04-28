import pandas as pd
from config import HIGHLIGHT_TOP_N, MOMENTUM_WINDOW


# ---------------------------------------------------------------------------
# Extractors — each accepts the ranked results list and returns plain dicts
# ---------------------------------------------------------------------------

def top_opportunities(ranked, n=HIGHLIGHT_TOP_N):
    """Return the n stocks with the highest scores."""
    return [
        {"ticker": r["ticker"], "score": r["score"], "signal": r["signal"]}
        for r in sorted(ranked, key=lambda r: r["score"], reverse=True)[:n]
    ]


def most_oversold(ranked, n=HIGHLIGHT_TOP_N):
    """Return the n stocks with the lowest RSI (most oversold)."""
    with_rsi = []
    for r in ranked:
        rsi_val = r["df"]["RSI"].iloc[-1] if "RSI" in r["df"].columns else None
        if rsi_val is not None and not pd.isna(rsi_val):
            with_rsi.append({"ticker": r["ticker"], "rsi": round(float(rsi_val), 1)})

    return sorted(with_rsi, key=lambda x: x["rsi"])[:n]


def biggest_movers(ranked, n=HIGHLIGHT_TOP_N, window=MOMENTUM_WINDOW):
    """Return the n stocks with the largest absolute % price change over `window` days."""
    movers = []
    for r in ranked:
        df = r["df"]
        if len(df) >= window + 1:
            start = float(df["Close"].iloc[-(window + 1)])
            end   = float(df["Close"].iloc[-1])
            pct   = round((end - start) / start * 100, 2)
            movers.append({"ticker": r["ticker"], "pct_change": pct, "window": window})

    # Sort by absolute magnitude so big drops also surface, then return top n by gain
    return sorted(movers, key=lambda x: x["pct_change"], reverse=True)[:n]


# ---------------------------------------------------------------------------
# Printer
# ---------------------------------------------------------------------------

def print_highlights(ranked, n=HIGHLIGHT_TOP_N):
    opportunities = top_opportunities(ranked, n)
    oversold      = most_oversold(ranked, n)
    movers        = biggest_movers(ranked, n)

    print("\n🔥 Top Opportunities:")
    for i, s in enumerate(opportunities, 1):
        print(f"  {i}. {s['ticker']}  (Score: {s['score']} — {s['signal']})")

    print("\n📉 Most Oversold:")
    if oversold:
        for s in oversold:
            print(f"  {s['ticker']}  (RSI: {s['rsi']})")
    else:
        print("  No RSI data available.")

    print("\n🚀 Biggest Movers:")
    if movers:
        for s in movers:
            sign = "+" if s["pct_change"] >= 0 else ""
            print(f"  {s['ticker']}  ({sign}{s['pct_change']}% last {s['window']} days)")
    else:
        print("  Not enough price history.")
