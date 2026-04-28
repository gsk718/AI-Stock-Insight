import pandas as pd
from config import (
    MA_SHORT, MA_LONG,
    RSI_OVERSOLD, RSI_OVERBOUGHT,
    MOMENTUM_WINDOW, MOMENTUM_STRONG_THRESHOLD,
    VOLATILITY_WINDOW, VOLATILITY_HIGH_CV,
)


def compute_score(df):
    """
    Scores the ticker on four independent factors. Each factor contributes
    a signed integer; they are summed into a single 'Score' column on the df.

    Factor          Condition                              Points
    ──────────────────────────────────────────────────────────────
    Trend           MA_SHORT > MA_LONG                    +1 / -1
    RSI             < RSI_OVERSOLD  (oversold)            +2
                    > RSI_OVERBOUGHT (overbought)         -2
    Momentum        N-day % change > threshold            +1
                    N-day % change < 0                    -1
    Volatility      20-day CoV > VOLATILITY_HIGH_CV       -1  (risk penalty)
    ──────────────────────────────────────────────────────────────
    Possible range: -5 to +4
    """
    latest = df.iloc[-1]
    score  = 0

    ma_short_col = f'MA{MA_SHORT}'
    ma_long_col  = f'MA{MA_LONG}'

    # --- Trend: short MA vs long MA ---
    if pd.notna(latest.get(ma_short_col)) and pd.notna(latest.get(ma_long_col)):
        score += 1 if latest[ma_short_col] > latest[ma_long_col] else -1

    # --- RSI: oversold / overbought with stronger weighting ---
    if pd.notna(latest.get('RSI')):
        if latest['RSI'] < RSI_OVERSOLD:
            score += 2   # oversold — potential reversal
        elif latest['RSI'] > RSI_OVERBOUGHT:
            score -= 2   # overbought — likely pullback

    # --- Momentum: N-day price percentage change ---
    if len(df) >= MOMENTUM_WINDOW + 1:
        momentum_pct = (
            (df['Close'].iloc[-1] - df['Close'].iloc[-(MOMENTUM_WINDOW + 1)])
            / df['Close'].iloc[-(MOMENTUM_WINDOW + 1)] * 100
        )
        if momentum_pct > MOMENTUM_STRONG_THRESHOLD:
            score += 1   # strong upward momentum
        elif momentum_pct < 0:
            score -= 1   # any negative momentum is a warning

    # --- Volatility: coefficient of variation over recent window ---
    if len(df) >= VOLATILITY_WINDOW:
        recent = df['Close'].tail(VOLATILITY_WINDOW)
        cv = recent.std() / recent.mean()
        if cv > VOLATILITY_HIGH_CV:
            score -= 1   # high price swings increase risk

    df['Score'] = score
    return df


def signal_label(score):
    if score >= 3:
        return "Strong Buy"
    if score >= 1:
        return "Buy"
    if score == 0:
        return "Neutral"
    if score >= -2:
        return "Sell"
    return "Strong Sell"
