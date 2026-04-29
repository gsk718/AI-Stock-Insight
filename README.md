# AI Stock Insight

AI Stock Insight is an AI-powered stock analysis system that transforms raw market data into structured insights using a data pipeline, technical indicators, and LLM-based reasoning.

The project simulates a lightweight quantitative research engine. It fetches historical stock data, processes it through technical indicators such as RSI, MACD, and moving averages, and then applies a scoring system to evaluate trading signals. Finally, it uses an LLM to generate natural language insights that summarize market conditions and potential opportunities.

The goal of this project is to combine traditional financial analysis techniques with modern AI reasoning to create a more intuitive understanding of market behavior.

---

## Tech Stack

- Python (core engine)
- Pandas / NumPy (data processing)
- yFinance (market data ingestion)
- Matplotlib / Plotly (data visualization)
- OpenAI API (LLM-based reasoning and insights)

---

## Features

- Automated stock data pipeline using yFinance
- Technical indicator generation (RSI, MACD, moving averages)
- Signal scoring system for evaluating market conditions
- AI-generated summaries and trading insights
- Visual charts for price action and indicators

---

## Project Structure

Main files in this project:

- main.py — Entry point of the application  
- pipeline.py — Handles stock data ingestion  
- indicators.py — Computes technical indicators  
- scoring.py — Evaluates buy/sell/hold signals  
- ai_insight.py — Generates AI-powered analysis  
- config.py — Stores configuration and constants  
- results.csv — Output data from runs  
- requirements.txt — Project dependencies  

---

## Setup Instructions

Clone the repository:

git clone https://github.com/gsk718/AI-Stock-Insight.git
cd AI-Stock-Insight

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the project:

python main.py

---

## How It Works

1. Fetch stock data using yFinance  
2. Calculate technical indicators (RSI, MACD, moving averages)  
3. Apply scoring logic to generate signals  
4. Pass structured data into an LLM for interpretation  
5. Output insights and visual charts  

















