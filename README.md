# Requirements
    Python 3

# Installation
    python -m venv .venv
    . .venv/bin/activate
    pip3 install -r requirements.txt

# Usage
    cd excelsior
    python3 cache.py
    python3 analysis.py

# Default Arguments
    python3 cache.py --help. Running with default arguments downloads data for all stocks in all US markets from the beginning of time, this may take a couple of hours.
    python3 analysis.py --help. Outputs 30 tickers with the best linear fit, and 30 with the best polynomial fit (2nd degree), from 2000 to 2023, and uses SPY as the benchmark to beat.
