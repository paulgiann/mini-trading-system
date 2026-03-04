import json
import pytest

from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger
from main import process_messages


def test_fix_parser_parses_order_with_pipe():
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|44=10.5|10=128"
    msg = FixParser().parse(raw)
    assert msg["35"] == "D"
    assert msg["55"] == "AAPL"
    assert msg["54"] == "1"
    assert msg["38"] == "100"


def test_fix_parser_parses_order_with_soh():
    soh = "\x01"
    raw = f"8=FIX.4.2{soh}35=D{soh}55=MSFT{soh}54=2{soh}38=10{soh}40=1{soh}10=999{soh}"
    msg = FixParser().parse(raw)
    assert msg["55"] == "MSFT"
    assert msg["54"] == "2"


def test_fix_parser_missing_required_tag_raises():
    raw = "8=FIX.4.2|35=D|55=AAPL|38=100|40=1|10=128"
    with pytest.raises(ValueError):
        FixParser().parse(raw)


def test_fix_parser_quote_validation():
    raw = "8=FIX.4.2|35=S|55=AAPL|132=100|133=101|10=1"
    msg = FixParser().parse(raw)
    assert msg["35"] == "S"


def test_order_transitions_allowed_and_blocked(capsys):
    o = Order("AAPL", 10, "1")
    assert o.state == OrderState.NEW

    assert o.transition(OrderState.ACKED) is True
    assert o.state == OrderState.ACKED

    assert o.transition(OrderState.NEW) is False
    assert o.state == OrderState.ACKED

    captured = capsys.readouterr().out
    assert "Transition not allowed" in captured


def test_risk_engine_rejects_oversize():
    r = RiskEngine(max_order_size=100)
    o = Order("AAPL", 101, "1")
    with pytest.raises(ValueError):
        r.check(o)


def test_risk_engine_rejects_position_limit():
    r = RiskEngine(max_order_size=1000, max_position=50)
    r.positions["AAPL"] = 40
    o = Order("AAPL", 20, "1")
    with pytest.raises(ValueError):
        r.check(o)


def test_risk_engine_updates_position():
    r = RiskEngine()
    o1 = Order("AAPL", 10, "1")
    r.update_position(o1)
    assert r.positions["AAPL"] == 10

    o2 = Order("AAPL", 5, "2")
    r.update_position(o2)
    assert r.positions["AAPL"] == 5


def test_logger_singleton_and_save(tmp_path):
    p = tmp_path / "events.json"

    l1 = Logger(path=str(p))
    l2 = Logger(path="ignored.json")
    assert l1 is l2

    l1.log("TestEvent", {"x": 1})
    l1.save()

    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data[-1]["type"] == "TestEvent"


def test_integration_process_messages_writes_events(tmp_path):
    p = tmp_path / "events.json"
    raws = [
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=10|40=1|10=1",
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=5000|40=1|10=2",
    ]
    orders = process_messages(raws, events_path=str(p))
    assert len(orders) == 2

    events = json.loads(p.read_text(encoding="utf-8"))
    types = [e["type"] for e in events]
    assert "OrderCreated" in types
    assert "OrderFilled" in types
    assert "OrderRejected" in types
