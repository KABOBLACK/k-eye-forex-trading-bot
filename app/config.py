from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    market: str = "Forex"
    starting_balance: float = 5.0
    fast_ema: int = 9
    slow_ema: int = 21
    rsi_period: int = 14
    risk_per_trade: float = 0.01
    max_positions: int = 1
    live_trading: bool = False


settings = Settings()
