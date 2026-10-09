"""Application package for the K-Eye Forex trading simulator."""

from .config import settings
from .market_data import PriceSeries
from .indicators import calculate_ema, calculate_rsi
from .risk import RiskManager, calculate_position_size
from .execution import Trade, PaperBroker
from .simulator import StrategySignal, generate_signal

__all__ = [
    "settings",
    "PriceSeries",
    "calculate_ema",
    "calculate_rsi",
    "RiskManager",
    "calculate_position_size",
    "Trade",
    "PaperBroker",
    "StrategySignal",
    "generate_signal",
]
