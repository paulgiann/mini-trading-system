from __future__ import annotations

from dataclasses import dataclass, field

from order import Order


@dataclass
class RiskEngine:
    max_order_size: int = 1000
    max_position: int = 2000
    positions: dict[str, int] = field(default_factory=dict)

    def check(self, order: Order) -> bool:
        if order.qty <= 0:
            raise ValueError("Order qty must be > 0")

        if order.qty > self.max_order_size:
            raise ValueError(f"Order size {order.qty} exceeds max_order_size {self.max_order_size}")

        if order.side not in {"1", "2"}:
            raise ValueError("Invalid side. Expected '1' (Buy) or '2' (Sell).")

        cur = self.positions.get(order.symbol, 0)
        signed = order.qty if order.side == "1" else -order.qty
        projected = cur + signed

        if abs(projected) > self.max_position:
            raise ValueError(
                f"Projected position {projected} exceeds max_position {self.max_position} for {order.symbol}"
            )

        return True

    def update_position(self, order: Order) -> None:
        cur = self.positions.get(order.symbol, 0)
        signed = order.qty if order.side == "1" else -order.qty
        self.positions[order.symbol] = cur + signed
