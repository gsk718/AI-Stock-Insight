from indicators import fetch_stock_data, generate_signals, compute_rsi
from scoring import compute_score, signal_label


def analyze_ticker(ticker):
    df = fetch_stock_data(ticker)
    df = generate_signals(df)
    df = compute_rsi(df)
    df = compute_score(df)
    score = int(df['Score'].iloc[-1])
    signal = signal_label(score)
    return {"ticker": ticker, "score": score, "signal": signal, "df": df}


def rank_tickers(tickers):
    results = []
    for ticker in tickers:
        print(f"  Analyzing {ticker}...")
        try:
            results.append(analyze_ticker(ticker))
        except Exception as e:
            print(f"  Warning: skipping {ticker} — {e}")

    results.sort(key=lambda r: r['score'], reverse=True)
    return results


def print_rankings(ranked, top_n=10):
    print("\n" + "=" * 40)
    print(f"  Top {min(top_n, len(ranked))} Stocks by Score")
    print("=" * 40)
    for i, r in enumerate(ranked[:top_n], start=1):
        print(f"{i:>2}. {r['ticker']:<6} — Score: {r['score']:>2}  ({r['signal']})")
    print("=" * 40)
