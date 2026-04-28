import os
import sqlite3
from datetime import date
import pandas as pd
from config import STORAGE_BACKEND, CSV_FILE, SQLITE_FILE, SQLITE_TABLE


def _to_dataframe(results):
    """Convert pipeline result dicts to a flat DataFrame row per ticker."""
    today = date.today().isoformat()
    return pd.DataFrame([
        {
            "date":   today,
            "ticker": r["ticker"],
            "score":  r["score"],
            "signal": r["signal"],
        }
        for r in results
    ])


def _save_to_csv(df):
    write_header = not os.path.exists(CSV_FILE)
    df.to_csv(CSV_FILE, mode="a", header=write_header, index=False)
    print(f"  Results appended to {CSV_FILE}")


def _save_to_sqlite(df):
    with sqlite3.connect(SQLITE_FILE) as conn:
        df.to_sql(SQLITE_TABLE, conn, if_exists="append", index=False)
    print(f"  Results appended to {SQLITE_FILE} (table: {SQLITE_TABLE})")


def save_results(results):
    """Persist ranked results using the backend defined in config.STORAGE_BACKEND."""
    if not results:
        return

    df = _to_dataframe(results)

    if STORAGE_BACKEND == "sqlite":
        _save_to_sqlite(df)
    else:
        _save_to_csv(df)
