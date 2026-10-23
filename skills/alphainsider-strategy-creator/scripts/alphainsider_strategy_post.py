#!/usr/bin/env python3
"""Agent CLI helper for opt-in AlphaInsider strategy timeline posts.

Run it as a command: ``init``, ``prepare``, ``check``, then ``post``. It is
importable only so local tests can exercise it. ALPHAINSIDER_API_KEY is loaded
privately from the injected environment or the project's ``.env``; it is never
printed or written.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from http.client import HTTPException
from pathlib import Path
from typing import Any, Callable, Iterator


BASE_URL = "https://alphainsider.com/api"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_ERROR_RESPONSE_BYTES = 64 * 1024
MAX_ENV_BYTES = 1024 * 1024
MAX_INPUT_BYTES = 1024 * 1024
MAX_POST_CHARACTERS = 1200
MIN_SENTENCES = 3
DAILY_POST_LIMIT = 100
RETRY_DELAY_SECONDS = 5.0
CONFIG_NAME = "post_updates.json"
DEFAULT_BANNED_WORDS = [
    "AI", "artificial intelligence", "bot", "bots", "agent", "agents", "LLM",
    "GPT", "algorithm-generated", "automated post", "not financial advice",
    "not investment advice", "financial advice", "investment advice",
    "guaranteed", "guarantee", "risk-free", "paper trading", "paper-trading",
]
DEFAULT_ALLOWED_TERMS = [
    "ETF", "USD", "US", "NYSE", "NASDAQ", "RSI", "SMA", "EMA", "MACD", "ATR",
    "CPI", "GDP", "FOMC", "ET", "UTC", "EST", "EDT", "CEO", "IPO", "YTD",
]
EXIT_OK, EXIT_CHECK, EXIT_USAGE, EXIT_NO_POST, EXIT_FAILED = 0, 1, 2, 3, 4

_SAFE_ID = re.compile(r"[A-Za-z0-9._-]{1,100}")
_NUMBER = re.compile(r"(?<![\d.])(?:\d[\d,]*(?:\.\d+)?|\.\d+)")
_TICKER = re.compile(r"(?<![A-Za-z0-9])([A-Z]{2,6})(?:-USD|\.[A-Z])?(?![A-Za-z0-9])")
_SENTENCE_END = re.compile(r"[.!?]+(?=\s|$)")
_ID_KEYS = frozenset({"orders_still_open"})  # plus any key ending in _id or _ids
_REDACTED = "<redacted>"


class UsageError(Exception):
    """Invalid arguments, files, configuration, or credentials (exit 2)."""


class Refused(Exception):
    """Posting is not allowed for this run (exit 3)."""


class Failed(Exception):
    """An AlphaInsider request failed or returned unusable data (exit 4)."""


class RequestError(Failed):
    """A request failed; ``ambiguous`` means it may still have taken effect."""

    def __init__(self, message: str, ambiguous: bool) -> None:
        super().__init__(message)
        self.ambiguous = ambiguous


class CheckFailed(Exception):
    """The draft broke one or more posting rules (exit 1)."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("; ".join(problems))
        self.problems = problems


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Keep credentials on the canonical AlphaInsider origin."""

    def redirect_request(self, *_args: object, **_kwargs: object) -> None:
        return None


_URL_OPENER = urllib.request.build_opener(_NoRedirectHandler())


def _redact(text: str, api_key: str) -> str:
    return (text.replace(api_key, _REDACTED) if api_key else text)[:300]


def api_request(method: str, path: str, api_key: str, *, query: list[tuple[str, str]] | None = None,
                body: dict[str, Any] | None = None, timeout: float = 30.0) -> Any:
    """Send one AlphaInsider request and return its ``response`` payload."""
    url = f"{BASE_URL}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"
    headers = {"Accept": "application/json", "Authorization": api_key}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with _URL_OPENER.open(request, timeout=timeout) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        message = f"HTTP {exc.code}"
        try:
            decoded = json.loads(exc.read(MAX_ERROR_RESPONSE_BYTES).decode("utf-8"))
            if isinstance(decoded, dict) and decoded.get("response") is not None:
                message = f"HTTP {exc.code}: {decoded['response']}"
        except (HTTPException, OSError, TypeError, ValueError):
            pass
        raise RequestError(_redact(message, api_key), ambiguous=not 400 <= exc.code < 500) from None
    except (HTTPException, OSError, ValueError):
        raise RequestError("request failed or timed out", ambiguous=True) from None

    if len(payload) > MAX_RESPONSE_BYTES:
        raise RequestError("response exceeds the size limit", ambiguous=True)
    try:
        if "json" not in content_type.lower():
            raise ValueError
        decoded = json.loads(payload.decode("utf-8"))
    except ValueError:
        raise RequestError("response was not JSON", ambiguous=True) from None
    if not isinstance(decoded, dict):
        raise RequestError("invalid AlphaInsider response envelope", ambiguous=True)
    if not decoded.get("success"):
        raise RequestError(_redact(str(decoded.get("response")), api_key), ambiguous=False)
    return decoded.get("response")


def validate_project_root(project_root: Path) -> Path:
    resolved_root = Path(project_root).expanduser().resolve()
    if not resolved_root.is_dir():
        raise UsageError("project root must be an existing directory")
    skills_root = Path(__file__).resolve().parents[2]
    if resolved_root == skills_root or skills_root in resolved_root.parents:
        raise UsageError("refusing to use an installed skill directory")
    if not (resolved_root / "plan.md").is_file():
        raise UsageError("project root must contain plan.md")
    return resolved_root


def _env_file_value(project_root: Path, name: str) -> str | None:
    """Read one name from the project's .env without exposing the file."""
    path = project_root / ".env"
    if path.is_symlink():
        raise UsageError("refusing to read a symbolic-link .env")
    if not path.exists():
        return None
    if not path.is_file():
        raise UsageError(".env exists but is not a regular file")
    if path.stat().st_size > MAX_ENV_BYTES:
        raise UsageError(".env is too large to read safely")

    with path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() != name:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                try:
                    decoded = json.loads(value)
                except json.JSONDecodeError:
                    decoded = value[1:-1]
                if isinstance(decoded, str):
                    value = decoded
            elif len(value) >= 2 and value[0] == value[-1] == "'":
                value = value[1:-1]
            return value or None
    return None


def load_api_key(project_root: Path) -> str:
    value = os.environ.get("ALPHAINSIDER_API_KEY") or _env_file_value(project_root,
                                                                       "ALPHAINSIDER_API_KEY")
    if not value:
        raise UsageError("ALPHAINSIDER_API_KEY is not configured")
    if any(ord(character) < 0x21 or ord(character) > 0x7E for character in value):
        raise UsageError("ALPHAINSIDER_API_KEY is invalid")
    return value


def _read_text(path: Path) -> str:
    path = Path(path)
    if path.name.startswith(".env"):
        raise UsageError("refusing to read a .env file")
    with path.open("rb") as handle:
        data = handle.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise UsageError(f"{path.name} is too large")
    return data.decode("utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _check_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value):
        raise UsageError(f"{label} must match [A-Za-z0-9._-]{{1,100}}")
    return value


def _default_config() -> dict[str, Any]:
    return {"post_updates": False, "banned_words": list(DEFAULT_BANNED_WORDS),
            "allowed_terms": list(DEFAULT_ALLOWED_TERMS)}


def load_config(project_root: Path) -> dict[str, Any] | None:
    """Return the posting config, or None when the file is missing (posting off)."""
    path = project_root / CONFIG_NAME
    if not path.exists():
        return None
    data = _read_json(path)
    if not isinstance(data, dict):
        raise UsageError(f"{CONFIG_NAME} must contain a JSON object")
    config = _default_config()
    config["post_updates"] = data.get("post_updates") is True
    for name in ("banned_words", "allowed_terms"):
        value = data.get(name, config[name])
        if not isinstance(value, list) or not all(isinstance(i, str) and i.strip() for i in value):
            raise UsageError(f"{CONFIG_NAME} {name} must be a list of non-empty strings")
        config[name] = value
    return config


def _require_enabled(project_root: Path) -> dict[str, Any]:
    config = load_config(project_root)
    if config is None or not config["post_updates"]:
        raise Refused(f"timeline posts are off ({CONFIG_NAME} missing or not enabled)")
    return config


def init_config(project_root: Path) -> Path:
    """Create post_updates.json with posting off; never overwrite an existing file."""
    path = validate_project_root(project_root) / CONFIG_NAME
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(_default_config(), indent=2) + "\n")
    except FileExistsError:
        pass
    return path


def _decimal(value: Any, label: str) -> Decimal:
    try:
        if value is None or isinstance(value, bool):
            raise InvalidOperation
        number = Decimal(str(value))
    except InvalidOperation:
        raise Failed(f"invalid {label} in AlphaInsider response") from None
    if not number.is_finite():
        raise Failed(f"invalid {label} in AlphaInsider response")
    return number


def _pct(fraction: Decimal) -> float:
    return float(round(fraction * 100, 2))


def summarize_positions(positions: Any, strategy_value: Decimal) -> dict[str, Any]:
    """Return signed position weights as percentages of current strategy value."""
    if not isinstance(positions, list):
        raise Failed("unexpected getPositions response")
    merged: dict[str, dict[str, Any]] = {}
    cash = Decimal(0)
    for row in positions:
        if not isinstance(row, dict):
            raise Failed("unexpected getPositions response")
        amount = _decimal(row.get("amount"), "position amount")
        if row.get("security") == "":
            cash += amount
            continue
        symbol = str(row.get("symbol") or row.get("stock") or "")
        # Value at the current quote: bid for longs, ask for shorts, else stored price.
        quote = row.get("bid") if amount >= 0 else row.get("ask")
        if quote is None:
            quote = row.get("price")
        price = _decimal(quote, f"{symbol} price")
        name = str(row.get("name") or symbol)
        entry = merged.setdefault(symbol, {"symbol": symbol, "name": name, "weight": Decimal(0)})
        entry["weight"] += amount * price / strategy_value
    rows = sorted(merged.values(), key=lambda entry: abs(entry["weight"]), reverse=True)
    return {
        "positions": [{"symbol": entry["symbol"], "name": entry["name"],
                       "side": "short" if entry["weight"] < 0 else "long",
                       "pct_of_strategy": _pct(entry["weight"])} for entry in rows],
        "gross_pct": _pct(sum((abs(entry["weight"]) for entry in rows), Decimal(0))),
        "cash_pct": _pct(cash / strategy_value),
    }


def wait_for_orders(api_key: str, strategy_id: str, order_ids: list[str], max_wait: float,
                    interval: float, sleep: Callable[[float], None]) -> list[str]:
    """Poll open orders until the given ids are gone or max_wait elapses."""
    still_open = list(order_ids)
    for poll in range(int(max_wait // interval) + 1):
        if poll:
            sleep(interval)
        orders = api_request("GET", "/getOrders", api_key, query=[("strategy_id", strategy_id)])
        if not isinstance(orders, list):
            raise Failed("unexpected getOrders response")
        open_ids = {str(order.get("order_id")) for order in orders if isinstance(order, dict)}
        still_open = [order_id for order_id in order_ids if order_id in open_ids]
        if not still_open:
            break
    return still_open


def prepare(project_root: Path, strategy_id: str, run_id: str, order_ids: list[str],
            context_path: Path | None = None, max_wait: float = 300.0, interval: float = 15.0,
            *, sleep: Callable[[float], None] = time.sleep) -> Path:
    """Write posts/<run-id>.facts.json for a run that placed orders. GET requests only."""
    root = validate_project_root(project_root)
    _check_id(strategy_id, "strategy id")
    _check_id(run_id, "run id")
    if not 0 <= max_wait <= 3600 or not 1 <= interval <= 600:
        raise UsageError("--max-wait must be 0-3600 and --interval 1-600 seconds")
    if any(not order_id or len(order_id) > 100 for order_id in order_ids):
        raise UsageError("order ids must be 1-100 characters")
    _require_enabled(root)
    if not order_ids:
        raise Refused("this run placed no orders")
    posts_dir = root / "posts"
    if any((posts_dir / f"{run_id}{suffix}").exists() for suffix in (".lock", ".result.json")):
        raise Refused("this run already has a post lock or result")
    context: Any = {}
    if context_path is not None:
        context = _read_json(context_path)
        if not isinstance(context, dict):
            raise UsageError("--context must contain a JSON object")

    api_key = load_api_key(root)
    order_ids = list(dict.fromkeys(order_ids))
    still_open = wait_for_orders(api_key, strategy_id, order_ids, max_wait, interval, sleep)
    positions = api_request("GET", "/getPositions", api_key, query=[("strategy_id", strategy_id)])
    # Plural reads take the strategy_id[] form; a plain strategy_id is rejected.
    values = api_request("GET", "/getStrategyValues", api_key,
                         query=[("strategy_id[]", strategy_id)])
    match = next((item for item in (values if isinstance(values, list) else [])
                  if isinstance(item, dict) and item.get("strategy_id") == strategy_id), None)
    if match is None:
        raise Failed("strategy value not found in getStrategyValues response")
    strategy_value = _decimal(match.get("strategy_value"), "strategy value")
    if strategy_value == 0:
        raise Failed("strategy value is zero; position weights are unavailable")

    facts = {
        "strategy_id": strategy_id,
        "run_id": run_id,
        "order_ids": order_ids,
        "orders_no_longer_open": len(order_ids) - len(still_open),
        "orders_still_open": still_open,
        **summarize_positions(positions, strategy_value),
        "context": context,
        "prepared_at": _now_iso(),
    }
    posts_dir.mkdir(exist_ok=True)
    path = posts_dir / f"{run_id}.facts.json"
    _write_json(path, facts)
    return path


def load_facts(path: Path) -> dict[str, Any]:
    facts = _read_json(path)
    if not isinstance(facts, dict):
        raise UsageError("facts file must contain a JSON object")
    _check_id(facts.get("strategy_id"), "facts strategy_id")
    _check_id(facts.get("run_id"), "facts run_id")
    return facts


def _is_id_key(key: str) -> bool:
    return key in _ID_KEYS or key.endswith(("_id", "_ids"))


def _fact_values(value: Any, key: str = "") -> Iterator[Any]:
    """Yield keys and leaf values, skipping id-like keys whose characters are random."""
    if _is_id_key(key):
        return
    if isinstance(value, dict):
        for child_key, child in value.items():
            child_key = str(child_key)
            if not _is_id_key(child_key):
                yield child_key
            yield from _fact_values(child, child_key)
    elif isinstance(value, list):
        for item in value:
            yield from _fact_values(item, key)
    elif isinstance(value, (str, int, float)) and not isinstance(value, bool):
        yield value


def _number_token(match: re.Match[str]) -> str:
    return match.group(0).rstrip(",").replace(",", "")


def _fact_vocabulary(facts: dict[str, Any]) -> tuple[set[Decimal], set[str]]:
    numbers: set[Decimal] = set()
    terms: set[str] = set()
    for value in _fact_values(facts):
        if isinstance(value, str):
            numbers.update(Decimal(_number_token(m)) for m in _NUMBER.finditer(value))
            for match in _TICKER.finditer(value):
                terms.update(match.group(0, 1))
        elif math.isfinite(value):
            numbers.add(abs(Decimal(str(value))))
    return numbers, terms


def _number_backed(token: str, fact_numbers: set[Decimal]) -> bool:
    """Match within display rounding, also allowing fraction<->percent scaling."""
    value = Decimal(token)
    decimals = len(token.partition(".")[2])
    tolerance = Decimal(5).scaleb(-decimals - 1)
    return any(abs(value - candidate) <= tolerance
               for fact in fact_numbers for candidate in (fact, fact * 100, fact / 100))


def check_draft(text: str, facts: dict[str, Any], config: dict[str, Any]) -> list[str]:
    """Return every rule the draft breaks; an empty list means it may be posted."""
    text = text.strip()
    if not text:
        return ["draft is empty"]
    problems = []
    if len(text) > MAX_POST_CHARACTERS:
        problems.append(f"draft has {len(text)} characters; the limit is {MAX_POST_CHARACTERS}")
    sentences = sum(1 for part in _SENTENCE_END.split(text) if len(part.split()) >= 3)
    if sentences < MIN_SENTENCES:
        problems.append(f"draft has {sentences} sentences of 3+ words; "
                        f"at least {MIN_SENTENCES} are required")
    for phrase in config["banned_words"]:
        pattern = r"(?<!\w)" + r"\s+".join(map(re.escape, phrase.split())) + r"(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            problems.append(f"banned word or phrase: {phrase}")
    fact_numbers, fact_terms = _fact_vocabulary(facts)
    for token in dict.fromkeys(_number_token(m) for m in _NUMBER.finditer(text)):
        if not _number_backed(token, fact_numbers):
            problems.append(f"number not in the facts: {token}")
    known_terms = fact_terms | {term.upper() for term in config["allowed_terms"]}
    for term in dict.fromkeys(m.group(0, 1) for m in _TICKER.finditer(text)):
        if not known_terms.intersection(term):
            problems.append(f"ticker-like term not in the facts or allowed_terms: {term[0]}")
    return problems


def run_check(facts_path: Path, text_path: Path) -> int:
    """Check a draft without network access; return its character count."""
    facts_path = Path(facts_path).resolve()
    facts = load_facts(facts_path)
    config = None
    if facts_path.parent.name == "posts":
        config = load_config(facts_path.parent.parent)
    text = _read_text(text_path).strip()
    problems = check_draft(text, facts, config or _default_config())
    if problems:
        raise CheckFailed(problems)
    return len(text)


def find_post(api_key: str, strategy_id: str, text: str) -> dict[str, Any] | None:
    """Return a recent timeline post whose description equals the draft, if any."""
    query = [("strategy_id[]", strategy_id), ("type[]", "post"), ("limit", "20")]
    events = api_request("GET", "/getStrategyTimelines", api_key, query=query)
    if not isinstance(events, list):
        raise Failed("unexpected getStrategyTimelines response")
    for event in events:
        data = event.get("data") if isinstance(event, dict) else None
        description = data.get("description") if isinstance(data, dict) else None
        if isinstance(description, str) and description.strip() == text:
            return event
    return None


def _posts_in_last_day(posts_dir: Path, strategy_id: str) -> int:
    log_path = posts_dir / "posts.log"
    if not log_path.exists():
        return 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)
    count = 0
    with log_path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
                if (entry["status"] == "posted" and entry["strategy_id"] == strategy_id
                        and datetime.fromisoformat(entry["at"]) > cutoff):
                    count += 1
            except (KeyError, TypeError, ValueError):
                continue
    return count


def _record(posts_dir: Path, facts: dict[str, Any], status: str, text: str, event: Any = None,
            errors: list[str] | None = None) -> dict[str, Any]:
    """Write the run's result file and a posts.log line; return the printed summary."""
    event = event if isinstance(event, dict) else {}
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    now = _now_iso()
    result = {
        "status": status,
        "timeline_id": event.get("timeline_id"),
        "post_id": data.get("post_id"),
        "posted_at": None if status == "failed" else event.get("created_at") or now,
        "text": text,
    }
    if errors:
        result["errors"] = errors
    _write_json(posts_dir / f"{facts['run_id']}.result.json", result)
    entry = {"at": now, "status": status, "strategy_id": facts["strategy_id"],
             "run_id": facts["run_id"], "timeline_id": result["timeline_id"]}
    with (posts_dir / "posts.log").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    summary = {key: result[key] for key in ("status", "timeline_id", "post_id")}
    summary.update(run_id=facts["run_id"], already_posted=status == "already_posted")
    if errors:
        summary["errors"] = errors
    return summary


def post(project_root: Path, facts_path: Path, text_path: Path, *,
         sleep: Callable[[float], None] = time.sleep) -> tuple[int, dict[str, Any]]:
    """Post a checked draft at most once per run; return (exit code, summary)."""
    root = validate_project_root(project_root)
    config = _require_enabled(root)
    posts_dir = (root / "posts").resolve()
    facts_path = Path(facts_path).resolve()
    if facts_path.parent != posts_dir:
        raise UsageError("facts file must be inside <project>/posts")
    facts = load_facts(facts_path)
    strategy_id, run_id = facts["strategy_id"], facts["run_id"]
    if facts_path.name != f"{run_id}.facts.json":
        raise UsageError("facts file name does not match its run_id")
    text = _read_text(text_path).strip()
    problems = check_draft(text, facts, config)
    if problems:
        raise CheckFailed(problems)

    if (posts_dir / f"{run_id}.result.json").exists():
        raise Refused("already posted or attempted for this run")
    lock_path = posts_dir / f"{run_id}.lock"
    try:
        os.close(os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600))
    except FileExistsError:
        raise Refused("already posted or attempted for this run") from None

    # Keep the lock forever once a request may have posted; release it otherwise.
    keep_lock = False
    try:
        api_key = load_api_key(root)
        if _posts_in_last_day(posts_dir, strategy_id) >= DAILY_POST_LIMIT:
            raise Refused(f"daily limit of {DAILY_POST_LIMIT} posts reached for this strategy")
        existing = find_post(api_key, strategy_id, text)
        keep_lock = True
        if existing is not None:
            return EXIT_OK, _record(posts_dir, facts, "already_posted", text, existing)

        errors: list[str] = []
        body = {"strategy_id": strategy_id, "description": text}
        for attempt in range(2):
            try:
                created = api_request("POST", "/newPost", api_key, body=body)
            except RequestError as exc:
                errors.append(str(exc))
                if not exc.ambiguous or attempt == 1:
                    break
            else:
                return EXIT_OK, _record(posts_dir, facts, "posted", text, created)
            sleep(RETRY_DELAY_SECONDS)
            try:
                existing = find_post(api_key, strategy_id, text)
            except Failed as exc:
                errors.append(f"timeline check before retry failed: {exc}")
                break
            if existing is not None:
                return EXIT_OK, _record(posts_dir, facts, "posted", text, existing)
        return EXIT_FAILED, _record(posts_dir, facts, "failed", text, errors=errors)
    finally:
        if not keep_lock:
            lock_path.unlink(missing_ok=True)


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        self.exit(EXIT_USAGE, "error: invalid arguments; run with --help for usage\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = _SafeArgumentParser(description="Opt-in AlphaInsider strategy timeline posts.")
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init", help="Create post_updates.json (off) if missing.")
    init_parser.add_argument("--project-root", type=Path, required=True)
    prepare_parser = commands.add_parser("prepare", help="Write a facts file after a run.")
    prepare_parser.add_argument("--project-root", type=Path, required=True)
    prepare_parser.add_argument("--strategy-id", required=True)
    prepare_parser.add_argument("--run-id", required=True)
    prepare_parser.add_argument("--order-id", dest="order_ids", action="append", default=[])
    prepare_parser.add_argument("--context", type=Path, help="JSON object of run facts.")
    prepare_parser.add_argument("--max-wait", type=float, default=300.0)
    prepare_parser.add_argument("--interval", type=float, default=15.0)
    check_parser = commands.add_parser("check", help="Check a draft without network access.")
    check_parser.add_argument("--facts", type=Path, required=True)
    check_parser.add_argument("--text", type=Path, required=True)
    post_parser = commands.add_parser("post", help="Post a checked draft once per run.")
    post_parser.add_argument("--project-root", type=Path, required=True)
    post_parser.add_argument("--facts", type=Path, required=True)
    post_parser.add_argument("--text", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "init":
            print(init_config(args.project_root))
        elif args.command == "prepare":
            print(prepare(args.project_root, args.strategy_id, args.run_id, args.order_ids,
                          args.context, args.max_wait, args.interval))
        elif args.command == "check":
            print(f"check passed ({run_check(args.facts, args.text)} characters)")
        else:
            code, summary = post(args.project_root, args.facts, args.text)
            print(json.dumps(summary, indent=2))
            return code
    except CheckFailed as exc:
        print("check failed:\n" + "\n".join(f"- {problem}" for problem in exc.problems))
        return EXIT_CHECK
    except Refused as exc:
        print(f"no post: {exc}")
        return EXIT_NO_POST
    except Failed as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FAILED
    except (UsageError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    return EXIT_OK


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except Exception:  # noqa: BLE001 - credential-safe CLI boundary
        print("error: failed safely", file=sys.stderr)
        raise SystemExit(EXIT_FAILED) from None
