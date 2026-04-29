# AI Stock Insight

AI Stock Insight is an AI-powered stock analysis system that transforms raw market data into actionable insights using a full data pipeline, technical indicators, and LLM-based reasoning.

The project simulates a lightweight quantitative research engine. It pulls historical stock data, processes it through technical indicator calculations (RSI, MACD, moving averages), and then generates structured insights using AI. The goal is to combine financial analysis with modern AI reasoning to interpret market behavior.

---

## Tech Stack

- Python (core engine)
- Pandas / NumPy (data processing)
- yFinance (market data)
- Matplotlib / Plotly (visualization)
- OpenAI API (LLM reasoning)

---

## Features

- Stock data ingestion pipeline
- Technical indicators (RSI, MACD, moving averages)
- AI-generated insights and summaries
- Visual charts for price + indicators
- Signal scoring system

---

## Project Structure

AI-Stock-Insight/
├── main.py              # Entry point
├── pipeline.py          # Data pipeline
├── indicators.py        # Technical indicators
├── scoring.py           # Signal scoring logic
├── ai_insight.py        # LLM reasoning layer
├── config.py            # Config
├── results.csv
├── requirements.txt
└── README.md

---

## Setup

git clone https://github.com/gsk718/AI-Stock-Insight.git
cd AI-Stock-Insight

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py

---

## How It Works

- Fetch stock data via yFinance
- Compute technical indicators
- Score signals
- Generate AI interpretation
- Output insights + charts

---

## Future Improvements

- Real-time data streaming
- Backtesting engine
- Portfolio optimization
- Web dashboard
