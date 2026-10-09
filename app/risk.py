from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskManager:
    max_positions: int = 1
    risk_per_trade: float = 0.01

    def can_open_new_position(self, open_positions: int) -> bool:
        return open_positions < self.max_positions

    def calculate_position_size(self, account_balance: float, stop_distance: float) -> float:
        if account_balance <= 0:
            return 0.0
        if stop_distance <= 0:
            return 0.0
        risk_amount = account_balance * self.risk_per_trade
        return risk_amount / stop_distance


def calculate_position_size(account_balance: float, stop_distance: float, risk_per_trade: float = 0.01) -> float:
    """Calculate the units to trade based on risk budget and stop distance."""
    if account_balance <= 0:
        return 0.0
    if stop_distance <= 0:
        return 0.0
    risk_amount = account_balance * risk_per_trade
    return risk_amount / stop_distance


__all__ = ["RiskManager", "calculate_position_size"]
