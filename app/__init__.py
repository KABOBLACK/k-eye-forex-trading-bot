"""Application package for the K-Eye Forex trading simulator."""

from .config import settings
from .execution import PaperBroker, Trade
from .indicators import calculate_ema, calculate_rsi
from .market_data import PriceSeries, generate_sample_prices
from .reporting import SimulationReport, summarize_trades
from .risk import RiskManager, calculate_position_size
from .simulator import StrategySignal, SimulationResult, generate_signal, run_simulation

__all__ = [
    "settings",
    "PriceSeries",
    "generate_sample_prices",
    "calculate_ema",
    "calculate_rsi",
    "RiskManager",
    "calculate_position_size",
    "Trade",
    "PaperBroker",
    "StrategySignal",
    "SimulationResult",
    "SimulationReport",
    "generate_signal",
    "run_simulation",
    "summarize_trades",
]
