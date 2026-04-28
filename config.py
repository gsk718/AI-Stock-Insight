# ---------------------------------------------------------------------------
# Central configuration — change values here to tune the whole pipeline
# ---------------------------------------------------------------------------

# --- Data fetch ---
FETCH_PERIOD   = "6mo"
FETCH_INTERVAL = "1d"

# --- Indicators ---
RSI_PERIOD = 14
MA_SHORT   = 5
MA_LONG    = 20

# --- Scoring thresholds ---
RSI_OVERSOLD              = 30
RSI_OVERBOUGHT            = 70
MOMENTUM_WINDOW           = 5    # trading days
MOMENTUM_STRONG_THRESHOLD = 2.0  # % gain to count as strong positive momentum
VOLATILITY_WINDOW         = 20   # trading days
VOLATILITY_HIGH_CV        = 0.03 # std/mean above this triggers the risk penalty

# --- AI ---
OPENAI_MODEL      = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 300

# --- Highlights ---
HIGHLIGHT_TOP_N = 3   # how many stocks to show per highlight category

# --- API ---
DEFAULT_TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "AMZN", "META", "AMD", "NFLX", "INTC"]
API_HOST        = "0.0.0.0"
API_PORT        = 8000

# --- Storage ---
# Set STORAGE_BACKEND to "sqlite" to switch away from CSV
STORAGE_BACKEND = "csv"
CSV_FILE        = "results.csv"
SQLITE_FILE     = "results.db"
SQLITE_TABLE    = "results"
