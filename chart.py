import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import RSI_OVERSOLD, RSI_OVERBOUGHT


def plot_stock_with_insight(df, ticker, insight):
    # Row 1: price + MAs  |  Row 2: RSI  |  Row 3: AI insight table
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.50, 0.25, 0.25],
        specs=[
            [{"type": "scatter"}],
            [{"type": "scatter"}],
            [{"type": "table"}],
        ],
        vertical_spacing=0.06,
        subplot_titles=(f"{ticker} Price", "RSI", ""),
    )

    # --- Row 1: price, moving averages, buy/sell markers ---
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines',
                             name='Close', line=dict(color='royalblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA5'],  mode='lines',
                             name='MA5',   line=dict(color='orange', dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], mode='lines',
                             name='MA20',  line=dict(color='purple', dash='dot')), row=1, col=1)

    buys  = df[df['Signal'] == 'Buy']
    sells = df[df['Signal'] == 'Sell']
    fig.add_trace(go.Scatter(x=buys['Date'],  y=buys['Close'],  mode='markers',
                             marker=dict(color='green', size=8, symbol='triangle-up'),
                             name='Buy Signal'), row=1, col=1)
    fig.add_trace(go.Scatter(x=sells['Date'], y=sells['Close'], mode='markers',
                             marker=dict(color='red', size=8, symbol='triangle-down'),
                             name='Sell Signal'), row=1, col=1)

    # --- Row 2: RSI line ---
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines',
                             name='RSI', line=dict(color='darkorange'),
                             showlegend=True), row=2, col=1)

    # Overbought / oversold reference lines
    fig.add_hline(y=RSI_OVERBOUGHT, row=2, col=1,
                  line=dict(color='red',   dash='dash', width=1),
                  annotation_text=f"Overbought ({RSI_OVERBOUGHT})",
                  annotation_position="top right")
    fig.add_hline(y=RSI_OVERSOLD,   row=2, col=1,
                  line=dict(color='green', dash='dash', width=1),
                  annotation_text=f"Oversold ({RSI_OVERSOLD})",
                  annotation_position="bottom right")

    # Fix RSI axis to [0, 100] so the bands always read correctly
    fig.update_yaxes(range=[0, 100], row=2, col=1)

    # --- Row 3: AI insight table ---
    fig.add_trace(go.Table(
        header=dict(values=[f"AI Insight for {ticker}"], fill_color='lightgrey',
                    font=dict(size=13)),
        cells=dict(values=[[insight]], font=dict(size=12))
    ), row=3, col=1)

    fig.update_layout(
        height=900,
        title=dict(text=f"{ticker} — Price, RSI & AI Insight", font=dict(size=16)),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        yaxis2_title="RSI",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.show()
