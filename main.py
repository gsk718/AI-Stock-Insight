from pipeline import rank_tickers, print_rankings
from ai_insight import get_ai_insight
from chart import plot_stock_with_insight
from storage import save_results
from highlights import print_highlights


def main():
    raw = input("Enter stock tickers (comma-separated, e.g., AAPL, MSFT, NVDA): ")
    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]

    print(f"\nRunning batch analysis for {len(tickers)} ticker(s)...")
    ranked = rank_tickers(tickers)

    print_rankings(ranked)
    print_highlights(ranked)

    print("\nSaving results...")
    save_results(ranked)

    show_charts = input("\nShow AI insight & chart for top stocks? (y/n): ").strip().lower()
    if show_charts == 'y':
        for r in ranked[:min(3, len(ranked))]:
            ticker, df, signal, score = r['ticker'], r['df'], r['signal'], r['score']
            print(f"\nFetching AI insight for {ticker}...")
            try:
                insight = get_ai_insight(ticker, df, signal, score)
                print(f"AI insight: {insight}")
                plot_stock_with_insight(df, ticker, insight)
            except Exception as e:
                print(f"Could not generate insight/chart for {ticker}: {e}")


if __name__ == "__main__":
    main()
