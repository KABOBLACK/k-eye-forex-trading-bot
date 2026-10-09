from __future__ import annotations

from app.market_data import generate_sample_prices
from app.simulator import generate_signal


def test_generate_sample_prices_produces_values() -> None:
    sample = generate_sample_prices(length=10)
    assert len(sample.prices) == 10
    assert sample.prices[0] > 0


def test_generate_signal_buy_condition() -> None:
    prices = [1.0 + index * 0.01 for index in range(50)]
    signal = generate_signal(prices, fast_period=5, slow_period=10, rsi_period=14)
    assert signal.action in {"BUY", "SELL", "HOLD"}


def test_generate_signal_hold_when_not_enough_data() -> None:
    prices = [1.0, 1.1, 1.2]
    signal = generate_signal(prices, fast_period=5, slow_period=10, rsi_period=14)
    assert signal.action == "HOLD"
