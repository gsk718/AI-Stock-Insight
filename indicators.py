import yfinance as yf
import pandas as pd
from config import FETCH_PERIOD, FETCH_INTERVAL, MA_SHORT, MA_LONG, RSI_PERIOD


def fetch_stock_data(ticker, period=FETCH_PERIOD, interval=FETCH_INTERVAL):
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data found for {ticker}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df[['Close']].copy()
    df.reset_index(inplace=True)
    return df


def generate_signals(df):
    df[f'MA{MA_SHORT}'] = df['Close'].rolling(MA_SHORT).mean()
    df[f'MA{MA_LONG}']  = df['Close'].rolling(MA_LONG).mean()
    df['Signal'] = ""
    valid_idx = df[f'MA{MA_LONG}'].notna()
    df.loc[valid_idx & (df['Close'] > df[f'MA{MA_SHORT}']), 'Signal'] = "Buy"
    df.loc[valid_idx & (df['Close'] < df[f'MA{MA_SHORT}']), 'Signal'] = "Sell"
    return df


def compute_rsi(df, period=RSI_PERIOD):
    delta    = df['Close'].diff()
    gain     = delta.clip(lower=0)
    loss     = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs       = avg_gain / avg_loss.replace(0, float('nan'))
    df['RSI'] = 100 - (100 / (1 + rs))
    return df
