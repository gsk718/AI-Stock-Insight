import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import RSI_OVERSOLD, RSI_OVERBOUGHT


def plot_stock_with_insight(df, ticker, insight):
    # Row 1: price + MAs (left) | RSI (right)  |  Row 2: AI insight table (full width)
    fig = make_subplots(
        rows=2, cols=2,
        row_heights=[0.65, 0.35],
        column_widths=[0.6, 0.4],
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "table", "colspan": 2}, None],
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
        subplot_titles=(f"{ticker} Price", "RSI", ""),
    )

    # --- Row 1, Col 1: price, moving averages, buy/sell markers ---
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines',
                             name='Close', line=dict(color='royalblue', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA5'],  mode='lines',
                             name='MA5',   line=dict(color='#f0a500', width=1, dash='dot'),
                             opacity=0.7), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], mode='lines',
                             name='MA20',  line=dict(color='mediumpurple', width=1.5, dash='dash')), row=1, col=1)

    # Only mark crossover points (signal changes), not every day
    crossovers = df['Signal'] != df['Signal'].shift(1)
    buys  = df[crossovers & (df['Signal'] == 'Buy')]
    sells = df[crossovers & (df['Signal'] == 'Sell')]
    fig.add_trace(go.Scatter(x=buys['Date'],  y=buys['Close'],  mode='markers',
                             marker=dict(color='green', size=9, symbol='triangle-up',
                                         line=dict(color='darkgreen', width=1)),
                             name='Buy Signal'), row=1, col=1)
    fig.add_trace(go.Scatter(x=sells['Date'], y=sells['Close'], mode='markers',
                             marker=dict(color='red', size=9, symbol='triangle-down',
                                         line=dict(color='darkred', width=1)),
                             name='Sell Signal'), row=1, col=1)

    # --- Row 1, Col 2: RSI line ---
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines',
                             name='RSI', line=dict(color='darkorange', width=1.5),
                             showlegend=True), row=1, col=2)

    # Overbought / oversold reference lines
    fig.add_hline(y=RSI_OVERBOUGHT, row=1, col=2,
                  line=dict(color='red',   dash='dash', width=1),
                  annotation_text=f"Overbought ({RSI_OVERBOUGHT})",
                  annotation_position="top right")
    fig.add_hline(y=RSI_OVERSOLD,   row=1, col=2,
                  line=dict(color='green', dash='dash', width=1),
                  annotation_text=f"Oversold ({RSI_OVERSOLD})",
                  annotation_position="bottom right")

    # Fix RSI axis to [0, 100] so the bands always read correctly
    fig.update_yaxes(range=[0, 100], row=1, col=2)

    # --- Row 2: AI insight table (spans both columns) ---
    insight_lines = [line.strip() for line in insight.split('\n') if line.strip()]
    fig.add_trace(go.Table(
        header=dict(values=[f"AI Insight for {ticker}"], fill_color='lightgrey',
                    font=dict(size=13), align='left'),
        cells=dict(values=[insight_lines], font=dict(size=12), align='left',
                   height=28)
    ), row=2, col=1)

    fig.update_layout(
        height=850,
        title=dict(text=f"{ticker} — Price, RSI & AI Insight", font=dict(size=16)),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis2_title="Date",
        yaxis2_title="RSI",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    fig.update_xaxes(showgrid=True, gridcolor='#e8e8e8', linecolor='#cccccc', zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='#e8e8e8', linecolor='#cccccc', zeroline=False)
    fig.show()
