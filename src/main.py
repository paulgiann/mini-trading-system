from __future__ import annotations

from typing import Iterable, List

from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger


def process_messages(raw_messages: Iterable[str], events_path: str = "events.json") -> List[Order]:
    fix = FixParser()
    risk = RiskEngine()
    log = Logger()
    log.set_path(events_path)
    log.reset()

    orders: List[Order] = []

    for raw in raw_messages:
        msg = fix.parse(raw)

        if msg["35"] != "D":
            log.log("MessageIgnored", {"reason": "Unsupported MsgType", "35": msg["35"], "raw": raw})
            continue

        order = Order(symbol=msg["55"], qty=int(msg["38"]), side=msg["54"])
        orders.append(order)
        log.log("OrderCreated", msg)

        try:
            risk.check(order)
            order.transition(OrderState.ACKED)

            risk.update_position(order)
            order.transition(OrderState.FILLED)
            log.log("OrderFilled", {"symbol": order.symbol, "qty": order.qty, "side": order.side})
        except ValueError as e:
            order.transition(OrderState.REJECTED)
            log.log("OrderRejected", {"symbol": order.symbol, "qty": order.qty, "reason": str(e)})

    log.save()
    return orders


if __name__ == "__main__":
    raws = [
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|44=189.50|10=128",
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=5000|40=1|10=999",
        "8=FIX.4.2|35=S|55=AAPL|132=189.40|133=189.60|10=111",
    ]
    process_messages(raws, events_path="events.json")
