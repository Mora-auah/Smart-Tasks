"""Masking layer: every text sent to OpenAI must pass through here.

Original values stay in memory for the duration of one request only (TokenMap).
Same value -> same token within a request. Patterns can be toggled individually.
"""
import re

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){2,7}(?:[ ]?[A-Z0-9]{1,3})?\b")
_CARD = re.compile(r"\b\d(?:[ -]?\d){12,18}\b")
_ID = re.compile(r"(?<!\d)\d{9}(?!\d)")
_PHONE = re.compile(r"(?<![\w-])(?:\+972|972|0)[-\s]?\d{1,2}[-\s]?\d{3}[-\s]?\d{4}(?!\d)")
_ACCOUNT = re.compile(r"(?<!\d)\d{8,12}(?!\d)")
TOKEN_RE = re.compile(r"\[(?:PHONE|ID|ACCOUNT|CARD|EMAIL)_\d+\]")


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def israeli_id_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(digits):
        d = int(ch) * (1 if i % 2 == 0 else 2)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


class TokenMap:
    def __init__(self) -> None:
        self._by_value: dict[str, str] = {}
        self.by_token: dict[str, str] = {}
        self._counts: dict[str, int] = {}

    def token_for(self, kind: str, value: str) -> str:
        key = f"{kind}:{value}"
        if key not in self._by_value:
            self._counts[kind] = self._counts.get(kind, 0) + 1
            token = f"[{kind}_{self._counts[kind]}]"
            self._by_value[key] = token
            self.by_token[token] = value
        return self._by_value[key]


def mask(text: str, tokens: TokenMap, enabled: dict[str, bool] | None = None) -> str:
    on = {"phone": True, "id": True, "account": True, "card": True, "email": True}
    on.update(enabled or {})

    def sub(pattern: re.Pattern, kind: str, check=None):
        def repl(m: re.Match) -> str:
            raw = m.group(0)
            digits = re.sub(r"\D", "", raw)
            if check and not check(digits):
                return raw
            return tokens.token_for(kind, raw)

        return lambda t: pattern.sub(repl, t)

    steps = []
    if on["email"]:
        steps.append(sub(_EMAIL, "EMAIL"))
    if on["card"]:
        steps.append(sub(_CARD, "CARD", lambda d: 13 <= len(d) <= 19 and luhn_ok(d)))
    if on["account"]:
        steps.append(sub(_IBAN, "ACCOUNT"))
    if on["id"]:
        steps.append(sub(_ID, "ID", israeli_id_ok))
    if on["phone"]:
        steps.append(sub(_PHONE, "PHONE"))
    for step in steps:
        text = step(text)
    return text


def unmask(text: str, tokens: TokenMap) -> tuple[str, list[str]]:
    """Restore tokens. Returns (text, unknown_tokens the model invented)."""
    unknown: list[str] = []

    def repl(m: re.Match) -> str:
        t = m.group(0)
        if t in tokens.by_token:
            return tokens.by_token[t]
        unknown.append(t)
        return t

    return TOKEN_RE.sub(repl, text), unknown
