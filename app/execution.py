from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Trade:
    symbol: str
    side: str
    entry_price: float
    quantity: float
    stop_loss: float
    opened_at: int
    status: str = "OPEN"
    closed_at: Optional[int] = None
    exit_price: Optional[float] = None

    @property
    def pnl(self) -> Optional[float]:
        if self.exit_price is None:
            return None
        if self.side.upper() == "BUY":
            return (self.exit_price - self.entry_price) * self.quantity
        return (self.entry_price - self.exit_price) * self.quantity


@dataclass
class PaperBroker:
    balance: float
    max_positions: int = 1
    positions: List[Trade] = field(default_factory=list)

    def can_open_new_position(self) -> bool:
        return sum(1 for trade in self.positions if trade.status == "OPEN") < self.max_positions

    def open_trade(
        self,
        symbol: str,
        side: str,
        entry_price: float,
        quantity: float,
        stop_loss: float,
        timestamp: int,
    ) -> Optional[Trade]:
        if not self.can_open_new_position():
            return None

        trade = Trade(
            symbol=symbol,
            side=side.upper(),
            entry_price=float(entry_price),
            quantity=float(quantity),
            stop_loss=float(stop_loss),
            opened_at=int(timestamp),
        )
        self.positions.append(trade)
        return trade

    def close_trade(self, trade: Trade, exit_price: float, timestamp: int) -> float:
        trade.exit_price = float(exit_price)
        trade.closed_at = int(timestamp)
        trade.status = "CLOSED"

        pnl = trade.pnl or 0.0
        self.balance += pnl
        return pnl

    @property
    def open_trade_count(self) -> int:
        return sum(1 for trade in self.positions if trade.status == "OPEN")
