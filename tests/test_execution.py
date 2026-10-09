from app.execution import PaperBroker


def test_paper_broker_blocks_second_position() -> None:
    broker = PaperBroker(balance=5.0, max_positions=1)
    first = broker.open_trade("EURUSD", "BUY", 1.10, 0.5, 1.09, 1)
    second = broker.open_trade("EURUSD", "BUY", 1.12, 0.5, 1.11, 2)
    assert first is not None
    assert second is None
    assert broker.open_trade_count == 1


def test_paper_broker_close_updates_balance() -> None:
    broker = PaperBroker(balance=5.0, max_positions=1)
    trade = broker.open_trade("EURUSD", "BUY", 1.10, 1.0, 1.09, 1)
    assert trade is not None
    broker.close_trade(trade, 1.12, 2)
    assert trade.status == "CLOSED"
    assert broker.balance > 5.0
