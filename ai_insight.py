import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from config import OPENAI_MODEL, OPENAI_MAX_TOKENS

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")

client = OpenAI(api_key=api_key)


def build_prompt(ticker, df, signal, score):
    latest = df.iloc[-1]

    last_10_prices = df['Close'].tail(10).round(2).tolist()

    rsi = round(latest['RSI'], 1) if 'RSI' in df.columns and not pd.isna(latest['RSI']) else "N/A"

    ma_short = round(latest['MA5'],  2) if 'MA5'  in df.columns and not pd.isna(latest['MA5'])  else None
    ma_long  = round(latest['MA20'], 2) if 'MA20' in df.columns and not pd.isna(latest['MA20']) else None
    if ma_short and ma_long:
        direction = "Uptrend" if ma_short > ma_long else "Downtrend"
        trend = f"{direction} (MA5={ma_short}, MA20={ma_long})"
    else:
        trend = "Insufficient data"

    return (
        f"You are a financial analyst. Analyze the following data for {ticker}.\n\n"
        f"Ticker: {ticker}\n"
        f"Signal: {signal}\n"
        f"Score: {score} (scale: -5 to +4, higher is more bullish)\n"
        f"Trend: {trend}\n"
        f"RSI: {rsi}\n"
        f"Last 10 closing prices: {last_10_prices}\n\n"
        f"Respond as a numbered list with exactly 3 points, one per line, no extra blank lines:\n"
        f"1. Explain the current trend based on the moving averages and prices.\n"
        f"2. Explain why the score is high or low.\n"
        f"3. Assess the risk level.\n"
        f"Each point should be one concise sentence."
    )


def get_ai_insight(ticker, df, signal, score):
    prompt = build_prompt(ticker, df, signal, score)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=OPENAI_MAX_TOKENS
    )
    return response.choices[0].message.content.strip()
