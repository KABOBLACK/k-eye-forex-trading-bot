from app.reporting import summarize_trades


def test_summarize_trades_handles_empty_list() -> None:
    summary = summarize_trades([], 5.0)
    assert summary.total_trades == 0
    assert summary.final_balance == 5.0
