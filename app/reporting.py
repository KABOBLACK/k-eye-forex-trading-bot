from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationReport:
    total_trades: int
    win_rate: float
    net_pnl: float
    final_balance: float
    average_trade_pnl: float


def summarize_trades(trades, starting_balance: float) -> SimulationReport:
    """Summarize closed trades into a simple performance report."""
    closed = [trade for trade in trades if trade.status == "CLOSED" and trade.pnl is not None]
    if not closed:
        return SimulationReport(
            total_trades=0,
            win_rate=0.0,
            net_pnl=0.0,
            final_balance=starting_balance,
            average_trade_pnl=0.0,
        )

    net_pnl = sum(trade.pnl or 0.0 for trade in closed)
    winning = sum(1 for trade in closed if (trade.pnl or 0.0) > 0)
    average_trade_pnl = net_pnl / len(closed)

    return SimulationReport(
        total_trades=len(closed),
        win_rate=(winning / len(closed)) * 100.0,
        net_pnl=net_pnl,
        final_balance=starting_balance + net_pnl,
        average_trade_pnl=average_trade_pnl,
    )
