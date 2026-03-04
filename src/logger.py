from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any


class Logger:
    """
    Singleton logger.

    - Path is set on first construction and does NOT get overwritten by later Logger(...) calls.
    - Use set_path(...) explicitly when you want to redirect output (useful for tmp_path tests).
    """

    _instance: Logger | None = None

    def __new__(cls, path: str = "events.json"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, path: str = "events.json"):
        if getattr(self, "_initialized", False):
            return
        self.path = path
        self.events: list[dict[str, Any]] = []
        self._initialized = True

    def set_path(self, path: str) -> None:
        self.path = path

    def reset(self) -> None:
        self.events.clear()

    def log(self, event_type: str, data: dict[str, Any]) -> None:
        evt = {
            "ts": datetime.now(UTC).isoformat(),
            "type": event_type,
            "data": data,
        }
        self.events.append(evt)
        print(f"[LOG] {event_type} → {data}")

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)
