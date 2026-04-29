# AI Stock Insight

AI Stock Insight is an AI-powered stock analysis tool that generates insights, technical indicators, and visualizations from market data using a data pipeline and LLM reasoning.

---

## Tech Stack

- Python (core engine)
- Pandas / NumPy (data processing)
- yFinance (market data)
- Matplotlib / Plotly (visualization)
- OpenAI API (LLM insights)

---

## Features

- Stock data ingestion pipeline  
- Technical indicator generation (RSI, MACD, moving averages)  
- AI-generated market insights and summaries  
- Visual charts for price and indicators  
- Scoring system for evaluating stock signals  

---

## Project Structure

AI-Stock-Insight/
├── main.py              # Entry point
├── pipeline.py          # Data pipeline
├── indicators.py        # Technical indicators
├── scoring.py           # Signal scoring logic
├── ai_insight.py        # LLM-based analysis
├── config.py            # Config / constants
├── results.csv          # Output data
├── requirements.txt     # Dependencies
└── README.md            # Project documentation

---

## Setup

Clone the repository:

git clone https://github.com/gsk718/AI-Stock-Insight.git
cd AI-Stock-Insight

Create virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the project:

python main.py

---

## How It Works

- Fetches stock data using yFinance  
- Calculates technical indicators (RSI, MACD, moving averages)  
- Runs scoring logic on signals  
- Sends structured context to an LLM for reasoning  
- Outputs insights and charts  

---


