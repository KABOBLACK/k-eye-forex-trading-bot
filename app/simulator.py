from __future__ import annotations

from dataclasses import dataclass

from .config import settings
from .indicators import calculate_ema, calculate_rsi


@dataclass(frozen=True)
class StrategySignal:
    action: str
    reason: str


@dataclass
class SimulationResult:
    trades: list
    final_balance: float
    equity_curve: list[float]
    net_pnl: float


def generate_signal(prices, fast_period: int | None = None, slow_period: int | None = None, rsi_period: int | None = None) -> StrategySignal:
    """Generate a signal from EMA crossover plus RSI condition."""
    if not prices:
        return StrategySignal("HOLD", "No data available")

    fast_period = settings.fast_ema if fast_period is None else fast_period
    slow_period = settings.slow_ema if slow_period is None else slow_period
    rsi_period = settings.rsi_period if rsi_period is None else rsi_period

    if len(prices) < max(fast_period, slow_period, rsi_period):
        return StrategySignal("HOLD", "Not enough data")

    fast_ema = calculate_ema(prices, fast_period)[-1]
    slow_ema = calculate_ema(prices, slow_period)[-1]
    current_rsi = calculate_rsi(prices, rsi_period)[-1]

    if fast_ema > slow_ema and current_rsi < 70:
        return StrategySignal("BUY", "Fast EMA above slow EMA and RSI below overbought threshold")
    if fast_ema < slow_ema and current_rsi > 30:
        return StrategySignal("SELL", "Fast EMA below slow EMA and RSI above oversold threshold")
    return StrategySignal("HOLD", "Trend and RSI are not aligned")


def run_simulation(
    price_series,
    starting_balance: float,
    symbol: str = "EURUSD",
    fast_period: int | None = None,
    slow_period: int | None = None,
    rsi_period: int | None = None,
    risk_per_trade: float = 0.01,
    max_positions: int = 1,
    stop_loss_pct: float = 0.005,
):
    """Run a lightweight simulation loop over a price series."""
    prices = list(price_series)
    if not prices:
        return SimulationResult(trades=[], final_balance=starting_balance, equity_curve=[starting_balance], net_pnl=0.0)

    from .execution import PaperBroker
    from .risk import calculate_position_size

    broker = PaperBroker(balance=starting_balance, max_positions=max_positions)
    trades = []
    equity_curve = [starting_balance]

    for idx in range(len(prices)):
        window = prices[: idx + 1]
        signal = generate_signal(window, fast_period, slow_period, rsi_period)

        if signal.action == "BUY" and broker.can_open_new_position():
            entry_price = prices[idx]
            stop_distance = entry_price * stop_loss_pct
            quantity = calculate_position_size(starting_balance, stop_distance, risk_per_trade)
            if quantity > 0:
                trade = broker.open_trade(symbol, "BUY", entry_price, quantity, entry_price - stop_distance, idx)
                if trade is not None:
                    trades.append(trade)

        if signal.action == "SELL" and broker.can_open_new_position():
            entry_price = prices[idx]
            stop_distance = entry_price * stop_loss_pct
            quantity = calculate_position_size(starting_balance, stop_distance, risk_per_trade)
            if quantity > 0:
                trade = broker.open_trade(symbol, "SELL", entry_price, quantity, entry_price + stop_distance, idx)
                if trade is not None:
                    trades.append(trade)

        for open_trade in list(broker.positions):
            if open_trade.status != "OPEN":
                continue
            if open_trade.side == "BUY" and prices[idx] <= open_trade.stop_loss:
                pnl = broker.close_trade(open_trade, open_trade.stop_loss, idx)
                equity_curve.append(broker.balance + sum(t.pnl or 0.0 for t in broker.positions if t.status == "CLOSED"))
                continue
            if open_trade.side == "SELL" and prices[idx] >= open_trade.stop_loss:
                pnl = broker.close_trade(open_trade, open_trade.stop_loss, idx)
                equity_curve.append(broker.balance + sum(t.pnl or 0.0 for t in broker.positions if t.status == "CLOSED"))

    net_pnl = broker.balance - starting_balance
    return SimulationResult(trades=trades, final_balance=broker.balance, equity_curve=equity_curve, net_pnl=net_pnl)


__all__ = ["StrategySignal", "SimulationResult", "generate_signal", "run_simulation"]
