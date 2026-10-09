from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass
class PriceSeries:
    """Simple container for price data."""

    prices: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.prices is None:
            self.prices = []

    def add(self, price: float) -> None:
        self.prices.append(float(price))

    @property
    def last(self) -> float | None:
        return self.prices[-1] if self.prices else None

    def __len__(self) -> int:
        return len(self.prices)

    def __iter__(self):
        return iter(self.prices)


def generate_sample_prices(start: float = 1.1000, drift: float = 0.0005, volatility: float = 0.0015, length: int = 50) -> PriceSeries:
    """Create a deterministic synthetic price series for testing and demos."""
    prices: List[float] = []
    current = start
    for index in range(length):
        shock = (index % 7) * volatility / 10.0
        current = current * (1 + drift + shock / 100.0)
        prices.append(round(current, 5))
    return PriceSeries(prices)
