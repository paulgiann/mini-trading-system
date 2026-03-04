from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional


class Logger:
    """
    Singleton logger.

    - Path is set on first construction and does NOT get overwritten by later Logger(...) calls.
    - Use set_path(...) explicitly when you want to redirect output (useful for tmp_path tests).
    """
    _instance: Optional["Logger"] = None

    def __new__(cls, path: str = "events.json"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, path: str = "events.json"):
        if getattr(self, "_initialized", False):
            return
        self.path = path
        self.events: List[Dict[str, Any]] = []
        self._initialized = True

    def set_path(self, path: str) -> None:
        self.path = path

    def reset(self) -> None:
        self.events.clear()

    def log(self, event_type: str, data: Dict[str, Any]) -> None:
        evt = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "data": data,
        }
        self.events.append(evt)
        print(f"[LOG] {event_type} → {data}")

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)
