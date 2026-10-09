from __future__ import annotations

from app.market_data import generate_sample_prices
from app.simulator import generate_signal, run_simulation


def test_generate_sample_prices_produces_values() -> None:
    sample = generate_sample_prices(length=10)
    assert len(sample.prices) == 10
    assert sample.prices[0] > 0


def test_generate_signal_hold_when_not_enough_data() -> None:
    prices = [1.0, 1.1, 1.2]
    signal = generate_signal(prices, fast_period=5, slow_period=10, rsi_period=14)
    assert signal.action == "HOLD"


def test_run_simulation_returns_result() -> None:
    prices = [1.00 + idx * 0.0005 for idx in range(60)]
    result = run_simulation(prices, starting_balance=5.0, fast_period=5, slow_period=10, rsi_period=14)
    assert result.final_balance >= 0
    assert result.net_pnl <= result.final_balance
