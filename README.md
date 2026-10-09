# K-Eye Forex Trading Bot V1.0

This project is a Python-based paper trading simulator for learning algorithmic trading.

## Mission
Build a practical forex trading simulator focused on learning, adaptation, and robust risk management.

## Initial configuration
- Market: Forex
- Starting simulated balance: $5
- Trading mode: Paper trading
- Fast EMA: 9
- Slow EMA: 21
- RSI period: 14
- Risk budget: 1% per trade, where practical
- Maximum simultaneous positions: 1
- Live trading: Disabled

## V1.0 scope
- Market data processing
- Technical indicators
- Automated trading signals
- Risk management
- Simulated order execution
- Trade history
- Performance reporting
- Automated tests

## Project structure
- `app/` — core trading logic
- `tests/` — unit tests
- `requirements.txt` — Python dependencies

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Risk notice
This software is experimental. It does not guarantee profits and must not place real trades in V1. Historical results do not guarantee future performance.
