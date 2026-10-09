from __future__ import annotations

from typing import Iterable, List


def calculate_ema(values: Iterable[float], period: int) -> List[float]:
    """Calculate the exponential moving average for a series of values."""
    series = list(values)
    if not series:
        return []
    if period <= 0:
        raise ValueError("period must be greater than 0")

    alpha = 2.0 / (period + 1.0)
    ema_values: List[float] = []
    current_ema = series[0]

    for value in series:
        current_ema = value * alpha + current_ema * (1 - alpha)
        ema_values.append(current_ema)

    return ema_values


def calculate_rsi(values: Iterable[float], period: int = 14) -> List[float]:
    """Calculate RSI using Wilder's smoothing method."""
    series = list(values)
    if not series:
        return []
    if period <= 0:
        raise ValueError("period must be greater than 0")
    if len(series) < 2:
        return [50.0] * len(series)

    deltas = [series[idx] - series[idx - 1] for idx in range(1, len(series))]
    gains = [max(delta, 0.0) for delta in deltas]
    losses = [abs(min(delta, 0.0)) for delta in deltas]

    rsi_values = [50.0] * len(series)
    if len(deltas) < period:
        return rsi_values

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for idx in range(period, len(deltas) + 1):
        if avg_loss == 0:
            rsi = 100.0
        else:
            relative_strength = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + relative_strength))
        rsi_values[idx] = rsi

        if idx < len(deltas):
            avg_gain = ((avg_gain * (period - 1)) + gains[idx]) / period
            avg_loss = ((avg_loss * (period - 1)) + losses[idx]) / period

    return rsi_values
