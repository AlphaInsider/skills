#!/usr/bin/env python3
"""Small stdlib request helper for the AlphaInsider REST API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://alphainsider.com/api"

STRATEGY_ARRAY_QUERY_PATHS = {
    "/getStrategies",
    "/getStrategyValues",
    "/getRecommendedStrategies",
    "/getStrategySubscriptions",
    "/getStrategyTimelines",
}

STRATEGY_QUERY_PATHS = {
    "/getStrategyPerformance",
    "/getStrategyCalculation",
    "/getPositions",
    "/getOrders",
    "/getMaxOrderSize",
}

STRATEGY_BODY_PATHS = {
    "/updateStrategy",
    "/updateStrategyPrice",
    "/deleteStrategy",
    "/newStrategySubscription",
    "/deleteStrategySubscription",
    "/updateStrategySubscriptionNotifications",
    "/updateStrategyCalculation",
    "/deleteStrategyCalculation",
    "/newPost",
    "/previewPost",
    "/newOrder",
    "/newOrderAllocations",
    "/deleteOrder",
    "/newOrderWebhook",
}

BOT_ARRAY_QUERY_PATHS = {
    "/getBots",
    "/getBotAllocations",
}

BOT_QUERY_PATHS = {
    "/getBotInfo",
    "/getBotPerformance",
    "/getBotActivities",
}

BOT_BODY_PATHS = {
    "/updateBotSettings",
    "/updateBotBrokerKeys",
    "/updateBotNotifications",
    "/deleteBot",
    "/startBot",
    "/stopBot",
    "/resetBot",
    "/resetBotPerformance",
    "/updateBotAllocations",
}

BODY_TOKEN_PATHS = {
    "/verifyToken": "token",
    "/newOrderWebhook": "api_token",
}


def load_dotenv_values(cwd: str) -> dict[str, str]:
    values: dict[str, str] = {}
    path = os.path.join(cwd, ".env")
    if not os.path.isfile(path):
        return values

    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key:
                values[key] = value
    return values


def setting(name: str, dotenv_values: dict[str, str]) -> str | None:
    return os.environ.get(name) or dotenv_values.get(name)


def parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"expected key=value, got {value!r}")
    key, parsed_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("key cannot be empty")
    return key, parsed_value


def normalize_path(path: str) -> str:
    return path if path.startswith("/") else f"/{path}"


def has_query_key(query: list[tuple[str, str]], *names: str) -> bool:
    wanted = set(names)
    return any(key in wanted for key, _ in query)


def body_has_key(body: object, name: str) -> bool:
    return isinstance(body, dict) and name in body


def apply_defaults(
    path: str,
    method: str,
    query: list[tuple[str, str]],
    body: object,
    api_key: str | None,
    strategy_id: str | None,
    bot_id: str | None,
) -> object:
    if path in BODY_TOKEN_PATHS and api_key:
        field = BODY_TOKEN_PATHS[path]
        if body is None:
            body = {}
        if isinstance(body, dict) and field not in body:
            body[field] = api_key

    if strategy_id:
        if path in STRATEGY_ARRAY_QUERY_PATHS and not has_query_key(query, "strategy_id[]", "strategy_id"):
            query.append(("strategy_id[]", strategy_id))
        elif path in STRATEGY_QUERY_PATHS and not has_query_key(query, "strategy_id", "strategy_id[]"):
            query.append(("strategy_id", strategy_id))
        elif path in STRATEGY_BODY_PATHS and not body_has_key(body, "strategy_id"):
            if body is None:
                body = {}
            if isinstance(body, dict):
                body["strategy_id"] = strategy_id

    if bot_id:
        if path in BOT_ARRAY_QUERY_PATHS and not has_query_key(query, "bot_id[]", "bot_id"):
            query.append(("bot_id[]", bot_id))
        elif path in BOT_QUERY_PATHS and not has_query_key(query, "bot_id", "bot_id[]"):
            query.append(("bot_id", bot_id))
        elif path in BOT_BODY_PATHS and not body_has_key(body, "bot_id"):
            if body is None:
                body = {}
            if isinstance(body, dict):
                body["bot_id"] = bot_id

    return body


def build_request(args: argparse.Namespace) -> tuple[str, dict[str, str], bytes | None, object]:
    dotenv_values = load_dotenv_values(os.getcwd())
    api_key = setting("ALPHAINSIDER_API_KEY", dotenv_values)
    strategy_id = setting("ALPHAINSIDER_STRATEGY_ID", dotenv_values)
    bot_id = setting("ALPHAINSIDER_BOT_ID", dotenv_values)

    path = normalize_path(args.path)
    method = args.method.upper()
    query = list(args.query or [])
    body = json.loads(args.json) if args.json else None
    body = apply_defaults(path, method, query, body, api_key, strategy_id, bot_id)

    base_url = args.base_url.rstrip("/")
    url = f"{base_url}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"

    headers = {"Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    if api_key and path not in BODY_TOKEN_PATHS:
        headers["Authorization"] = api_key

    return url, headers, data, body


def print_dry_run(method: str, url: str, headers: dict[str, str], body: object) -> None:
    safe_headers = dict(headers)
    if "Authorization" in safe_headers:
        safe_headers["Authorization"] = "<redacted>"
    if isinstance(body, dict):
        body = dict(body)
        for field in ("token", "api_token"):
            if field in body:
                body[field] = "<redacted>"
    print(json.dumps({"method": method, "url": url, "headers": safe_headers, "body": body}, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Make a request to the AlphaInsider REST API.")
    parser.add_argument("method", help="HTTP method, such as GET or POST.")
    parser.add_argument("path", help="API path, such as /getStrategies.")
    parser.add_argument("--query", action="append", type=parse_key_value, help="Query parameter as key=value. Repeat as needed.")
    parser.add_argument("--json", help="JSON request body.")
    parser.add_argument("--base-url", default=BASE_URL, help=f"Base URL. Defaults to {BASE_URL}.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the request without sending it.")
    args = parser.parse_args()

    try:
        url, headers, data, body = build_request(args)
    except json.JSONDecodeError as exc:
        print(f"invalid --json: {exc}", file=sys.stderr)
        return 2

    method = args.method.upper()
    if args.dry_run:
        print_dry_run(method, url, headers, body)
        return 0

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        content_type = exc.headers.get("Content-Type", "")
        print(f"HTTP {exc.code}", file=sys.stderr)
    except urllib.error.URLError as exc:
        print(f"request failed: {exc.reason}", file=sys.stderr)
        return 1

    text = payload.decode("utf-8", errors="replace")
    if "application/json" in content_type:
        try:
            print(json.dumps(json.loads(text), indent=2))
        except json.JSONDecodeError:
            print(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
