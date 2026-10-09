from app.indicators import calculate_ema, calculate_rsi


def test_calculate_ema_returns_list() -> None:
    values = [1.0, 2.0, 3.0, 4.0]
    results = calculate_ema(values, 3)
    assert len(results) == len(values)
    assert results[0] > 0
    assert results[-1] > results[0]


def test_calculate_rsi_is_within_bounds() -> None:
    values = [44.0, 45.0, 46.0, 45.0, 44.0, 43.0, 42.5, 43.5, 44.0, 45.0]
    result = calculate_rsi(values, 3)
    assert len(result) == len(values)
    assert all(0 <= value <= 100 for value in result)
