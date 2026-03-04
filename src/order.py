from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()


@dataclass
class Order:
    symbol: str
    qty: int
    side: str
    state: OrderState = field(default=OrderState.NEW)
    order_id: Optional[str] = field(default=None)

    def transition(self, new_state: OrderState) -> bool:
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED, OrderState.CANCELED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED, OrderState.REJECTED},
            OrderState.FILLED: set(),
            OrderState.CANCELED: set(),
            OrderState.REJECTED: set(),
        }

        if new_state in allowed.get(self.state, set()):
            self.state = new_state
            print(f"Order {self.symbol} is now {self.state.name}")
            return True

        print(f"[WARN] Transition not allowed: {self.state.name} -> {new_state.name} (Order {self.symbol})")
        return False
