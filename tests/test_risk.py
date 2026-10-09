from app.risk import RiskManager, calculate_position_size


def test_risk_manager_allows_trade_when_positions_available() -> None:
    manager = RiskManager(max_positions=1, risk_per_trade=0.01)
    assert manager.can_open_new_position(0) is True
    assert manager.can_open_new_position(1) is False


def test_calculate_position_size_uses_risk_budget() -> None:
    size = calculate_position_size(5.0, 0.10, risk_per_trade=0.01)
    assert size > 0
    assert size == 0.5
