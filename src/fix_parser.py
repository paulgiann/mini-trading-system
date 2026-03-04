from __future__ import annotations


class FixParser:
    SOH = "\x01"

    def __init__(self, delimiter: str | None = None):
        self.delimiter = delimiter

    def parse(self, raw: str) -> dict[str, str]:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("FIX message must be a non-empty string")

        delim = self._detect_delimiter(raw)
        fields = [f for f in raw.strip().split(delim) if f]
        msg: dict[str, str] = {}

        for field in fields:
            if "=" not in field:
                raise ValueError(f"Invalid FIX field (missing '='): {field!r}")
            tag, val = field.split("=", 1)
            tag = tag.strip()
            if not tag:
                raise ValueError(f"Invalid FIX field (empty tag): {field!r}")
            msg[tag] = val

        self._require(msg, ["35"])

        msg_type = msg["35"]
        if msg_type == "D":
            self._validate_new_order_single(msg)
        elif msg_type == "S":
            self._validate_quote(msg)
        else:
            raise ValueError(f"Unsupported MsgType (35): {msg_type!r}")

        return msg

    def _detect_delimiter(self, raw: str) -> str:
        if self.delimiter:
            return self.delimiter
        if self.SOH in raw:
            return self.SOH
        return "|"

    def _require(self, msg: dict[str, str], tags: list[str]) -> None:
        missing = [t for t in tags if t not in msg or msg[t] == ""]
        if missing:
            raise ValueError(f"Missing required FIX tags: {missing}")

    def _validate_new_order_single(self, msg: dict[str, str]) -> None:
        self._require(msg, ["55", "54", "38", "40"])

        if msg["54"] not in {"1", "2"}:
            raise ValueError("Invalid Side (54). Expected '1' (Buy) or '2' (Sell).")

        try:
            qty = int(msg["38"])
        except ValueError as e:
            raise ValueError("Invalid OrderQty (38). Must be integer.") from e
        if qty <= 0:
            raise ValueError("Invalid OrderQty (38). Must be > 0.")

        ord_type = msg["40"]
        if ord_type not in {"1", "2"}:
            raise ValueError("Invalid OrdType (40). Expected '1' (Market) or '2' (Limit).")

        if ord_type == "2":
            self._require(msg, ["44"])
            try:
                px = float(msg["44"])
            except ValueError as e:
                raise ValueError("Invalid Price (44). Must be numeric.") from e
            if px <= 0:
                raise ValueError("Invalid Price (44). Must be > 0.")

    def _validate_quote(self, msg: dict[str, str]) -> None:
        self._require(msg, ["55", "132", "133"])
        try:
            bid = float(msg["132"])
            ask = float(msg["133"])
        except ValueError as e:
            raise ValueError("Invalid quote prices (132/133). Must be numeric.") from e
        if bid <= 0 or ask <= 0 or bid > ask:
            raise ValueError("Invalid quote: require 0 < bid <= ask.")


if __name__ == "__main__":
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|44=189.50|10=128"
    print(FixParser().parse(msg))
