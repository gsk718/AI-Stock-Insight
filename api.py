import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from pipeline import analyze_ticker, rank_tickers
from ai_insight import get_ai_insight
from storage import save_results
from highlights import top_opportunities, most_oversold, biggest_movers
from config import DEFAULT_TICKERS, API_HOST, API_PORT

app = FastAPI(
    title="Stock Analysis API",
    description="Fetch scores, signals, and AI insights for stocks.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class AnalysisResponse(BaseModel):
    ticker: str
    score: int
    signal: str
    insight: str


class StockRank(BaseModel):
    ticker: str
    score: int
    signal: str


class HighlightsResponse(BaseModel):
    top_opportunities: List[StockRank]
    most_oversold:     List[dict]
    biggest_movers:    List[dict]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/analyze", response_model=AnalysisResponse)
def analyze(
    ticker: str = Query(..., description="Stock ticker symbol, e.g. AAPL"),
):
    """Full analysis for a single ticker: score, signal, and AI insight."""
    ticker = ticker.upper()

    try:
        result = analyze_ticker(ticker)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    try:
        insight = get_ai_insight(result["ticker"], result["df"], result["signal"], result["score"])
    except Exception:
        insight = "AI insight unavailable."

    return AnalysisResponse(
        ticker=result["ticker"],
        score=result["score"],
        signal=result["signal"],
        insight=insight,
    )


@app.get("/top-stocks", response_model=List[StockRank])
def top_stocks(
    tickers: Optional[str] = Query(
        None,
        description="Comma-separated tickers to rank. Defaults to built-in watchlist.",
    ),
    top_n: int = Query(10, ge=1, le=50, description="Number of results to return."),
):
    """Batch analysis: rank tickers by score and return the top N."""
    ticker_list = (
        [t.strip().upper() for t in tickers.split(",") if t.strip()]
        if tickers
        else DEFAULT_TICKERS
    )

    ranked = rank_tickers(ticker_list)
    save_results(ranked)

    return [
        StockRank(ticker=r["ticker"], score=r["score"], signal=r["signal"])
        for r in ranked[:top_n]
    ]


@app.get("/highlights", response_model=HighlightsResponse)
def highlights(
    tickers: Optional[str] = Query(None, description="Comma-separated tickers. Defaults to watchlist."),
):
    """Return top opportunities, most oversold, and biggest movers."""
    ticker_list = (
        [t.strip().upper() for t in tickers.split(",") if t.strip()]
        if tickers
        else DEFAULT_TICKERS
    )

    ranked = rank_tickers(ticker_list)

    return HighlightsResponse(
        top_opportunities=[StockRank(**s) for s in top_opportunities(ranked)],
        most_oversold=most_oversold(ranked),
        biggest_movers=biggest_movers(ranked),
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("api:app", host=API_HOST, port=API_PORT, reload=True)
