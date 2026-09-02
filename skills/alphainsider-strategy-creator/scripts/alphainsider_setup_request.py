#!/usr/bin/env python3
"""Agent-only AlphaInsider REST wrapper that hides ALPHAINSIDER_API_KEY."""

from __future__ import annotations

if __name__ != "__main__":
    raise RuntimeError("alphainsider_setup_request.py is CLI-only; do not import it")

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.client import HTTPException
from pathlib import Path
from typing import Any


BASE_URL = "https://alphainsider.com/api"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_ERROR_RESPONSE_BYTES = 64 * 1024
MAX_REQUEST_BODY_BYTES = 2 * 1024 * 1024
MAX_ENV_BYTES = 1024 * 1024
_PRINTABLE_CONFIG = "ALPHAINSIDER_STRATEGY_ID"
_READABLE_NAMES = frozenset({"ALPHAINSIDER_API_KEY", _PRINTABLE_CONFIG})
_REDACTED = "<redacted>"
_ALLOWED_OPERATIONS = {
    "/verifyToken": frozenset({"GET"}),
    "/getUserInfo": frozenset({"GET"}),
    "/getStrategies": frozenset({"GET"}),
    "/getUserStrategies": frozenset({"GET"}),
    "/newStrategy": frozenset({"POST"}),
    "/updateStrategy": frozenset({"POST"}),
    "/deleteStrategy": frozenset({"POST"}),
    "/getStrategySubscriptions": frozenset({"GET"}),
    "/getAccountSubscription": frozenset({"GET"}),
    "/getPositions": frozenset({"GET"}),
    "/getOrders": frozenset({"GET"}),
    "/getStocks": frozenset({"GET"}),
    "/searchStocks": frozenset({"POST"}),
    "/getExchangeStatus": frozenset({"GET"}),
}


class _SetupRequestError(ValueError):
    """The setup request cannot be built or sent safely."""


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Keep credentials on the canonical AlphaInsider origin."""

    def redirect_request(self, *_args: object, **_kwargs: object) -> None:
        return None


_URL_OPENER = urllib.request.build_opener(_NoRedirectHandler())


def _validate_project_root(project_root: Path) -> Path:
    resolved_root = project_root.expanduser().resolve()
    if not resolved_root.is_dir():
        raise _SetupRequestError("project root must be an existing directory")
    skills_root = Path(__file__).resolve().parents[2]
    if resolved_root == skills_root or skills_root in resolved_root.parents:
        raise _SetupRequestError("refusing to use an installed skill directory")
    if not (resolved_root / "plan.md").is_file():
        raise _SetupRequestError("project root must contain plan.md")
    return resolved_root


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        self.exit(
            2,
            "error: invalid arguments; pass METHOD PATH or "
            "--print-config ALPHAINSIDER_STRATEGY_ID\n",
        )


def _configured_value(name: str, project_root: str) -> str | None:
    if name not in _READABLE_NAMES:
        raise _SetupRequestError(f"unsupported AlphaInsider setting: {name}")

    environment_value = os.environ.get(name)
    if environment_value:
        return environment_value

    path = Path(project_root) / ".env"
    if path.is_symlink():
        raise _SetupRequestError("refusing to read a symbolic-link .env")
    if not path.exists():
        return None
    if not path.is_file():
        raise _SetupRequestError(".env exists but is not a regular file")
    if path.stat().st_size > MAX_ENV_BYTES:
        raise _SetupRequestError(".env is too large to read safely")

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


def _validated_api_key(value: str | None) -> str | None:
    if value is None:
        return None
    if not value or any(
        ord(character) < 0x21 or ord(character) > 0x7E for character in value
    ):
        raise _SetupRequestError("ALPHAINSIDER_API_KEY is invalid")
    return value


def _parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected key=value")
    key, parsed_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("key cannot be empty")
    return key, parsed_value


def _normalize_path(path: str) -> str:
    normalized = path if path.startswith("/") else f"/{path}"
    parsed = urllib.parse.urlsplit(normalized)
    if (
        parsed.scheme
        or parsed.netloc
        or parsed.query
        or parsed.fragment
        or "\\" in normalized
        or any(
            ord(character) < 0x20 or ord(character) == 0x7F
            for character in normalized
        )
        or any(part in {"", ".", ".."} for part in normalized.split("/")[1:])
    ):
        raise _SetupRequestError("invalid AlphaInsider API path")
    return normalized


def _validate_operation(method: str, path: str) -> str:
    normalized_method = method.upper()
    allowed_methods = _ALLOWED_OPERATIONS.get(path)
    if allowed_methods is None or normalized_method not in allowed_methods:
        raise _SetupRequestError("operation is not allowed by the setup helper")
    return normalized_method


def _query_items(query: list[tuple[str, str]] | None) -> list[tuple[str, str]]:
    return list(query or ())


def _is_credential_key(key: object) -> bool:
    normalized = str(key).lower().removesuffix("[]").replace("-", "_")
    return normalized in {
        "accesskey",
        "accesstoken",
        "apikey",
        "authorization",
        "password",
        "refresh_token",
        "secret",
        "secretkey",
        "token",
    } or normalized.endswith(("_key", "_password", "_secret", "_token"))


def _credential_values(value: object) -> list[str]:
    secrets: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if _is_credential_key(key) and isinstance(item, str) and item:
                secrets.append(item)
            else:
                secrets.extend(_credential_values(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            secrets.extend(_credential_values(item))
    return secrets


def _redact(value: object, secrets: tuple[str, ...]) -> object:
    if isinstance(value, dict):
        return {
            key: _REDACTED
            if _is_credential_key(key)
            else _redact(item, secrets)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item, secrets) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact(item, secrets) for item in value)
    if isinstance(value, str):
        for secret in sorted(set(secrets), key=len, reverse=True):
            if secret:
                value = value.replace(secret, _REDACTED)
        return value
    if isinstance(value, bytes):
        for secret in sorted(set(secrets), key=len, reverse=True):
            if secret:
                value = value.replace(secret.encode(), _REDACTED.encode())
        return value
    return value


def _collect_secrets(
    api_key: str | None,
    query_items: list[tuple[str, str]],
    body: object,
) -> tuple[str, ...]:
    secrets = _credential_values(body)
    secrets.extend(
        value for key, value in query_items if _is_credential_key(key) and value
    )
    if api_key:
        secrets.append(api_key)
    return tuple(dict.fromkeys(secrets))


def _build_request(
    method: str,
    path: str,
    *,
    query: list[tuple[str, str]] | None,
    body: object,
    api_key: str | None,
) -> tuple[urllib.request.Request, object, tuple[str, ...]]:
    normalized_path = _normalize_path(path)
    normalized_method = _validate_operation(method, normalized_path)
    query_items = _query_items(query)
    prepared_body = dict(body) if isinstance(body, dict) else body
    url = f"{BASE_URL}{normalized_path}"
    if query_items:
        url = f"{url}?{urllib.parse.urlencode(query_items)}"

    headers = {"Accept": "application/json"}
    data = None
    if prepared_body is not None:
        data = json.dumps(prepared_body).encode("utf-8")
        if len(data) > MAX_REQUEST_BODY_BYTES:
            raise _SetupRequestError("JSON request body is too large")
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["Authorization"] = api_key

    return (
        urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=normalized_method,
        ),
        prepared_body,
        _collect_secrets(api_key, query_items, prepared_body),
    )


def _api_error(
    payload: bytes,
    content_type: str,
    status_code: int,
    secrets: tuple[str, ...],
) -> str:
    if "json" in content_type.lower():
        try:
            decoded = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
        else:
            if isinstance(decoded, dict) and decoded.get("response") is not None:
                return str(_redact(decoded["response"], secrets))
    return f"HTTP {status_code}"


def _send_request(
    prepared: urllib.request.Request,
    secrets: tuple[str, ...],
    timeout: float,
) -> Any:
    try:
        with _URL_OPENER.open(prepared, timeout=timeout) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)
            if len(payload) > MAX_RESPONSE_BYTES:
                raise _SetupRequestError("response exceeds the configured size limit")
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        try:
            payload = exc.read(MAX_ERROR_RESPONSE_BYTES + 1)
            if len(payload) > MAX_ERROR_RESPONSE_BYTES:
                payload = b""
            content_type = exc.headers.get("Content-Type", "")
        except (HTTPException, OSError, TypeError, ValueError):
            payload = b""
            content_type = ""
        raise _SetupRequestError(
            _api_error(payload, content_type, exc.code, secrets)
        ) from None
    except _SetupRequestError:
        raise
    except (HTTPException, OSError, TypeError, UnicodeError, ValueError):
        raise _SetupRequestError("request failed") from None

    if "json" not in content_type.lower():
        raise _SetupRequestError("binary responses are not supported")
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise _SetupRequestError("invalid JSON response") from None
    if not isinstance(decoded, dict):
        raise _SetupRequestError("invalid AlphaInsider response envelope")
    if not decoded.get("success"):
        raise _SetupRequestError(
            str(_redact(decoded.get("response", "Request failed."), secrets))
        )
    if "response" not in decoded:
        raise _SetupRequestError("AlphaInsider response is missing response data")
    return _redact(decoded["response"], secrets)


def _print_dry_run(
    prepared: urllib.request.Request,
    body: object,
    secrets: tuple[str, ...],
) -> None:
    print(
        json.dumps(
            {
                "method": prepared.get_method(),
                "url": _redact(prepared.full_url, secrets),
                "headers": _redact(dict(prepared.header_items()), secrets),
                "body": _redact(body, secrets),
            },
            indent=2,
        )
    )


def _cli_body(inline_json: str | None, read_stdin: bool) -> object:
    if read_stdin:
        payload = sys.stdin.buffer.read(MAX_REQUEST_BODY_BYTES + 1)
        if len(payload) > MAX_REQUEST_BODY_BYTES:
            raise _SetupRequestError("JSON request body is too large")
        try:
            source = payload.decode("utf-8")
        except UnicodeDecodeError:
            raise _SetupRequestError("JSON request body must be UTF-8") from None
    else:
        source = inline_json
    if source is None:
        return None
    try:
        body = json.loads(source)
    except json.JSONDecodeError as exc:
        raise _SetupRequestError(f"invalid JSON at position {exc.pos}") from None
    if inline_json is not None and _credential_values(body):
        raise _SetupRequestError(
            "credential-bearing JSON must be provided with --json-stdin"
        )
    return body


def _print_config(name: str, project_root: str) -> int:
    if name != _PRINTABLE_CONFIG:
        print(
            "error: --print-config accepts only ALPHAINSIDER_STRATEGY_ID",
            file=sys.stderr,
        )
        return 2
    value = _configured_value(name, project_root)
    if not value:
        print(f"error: {name} is not configured", file=sys.stderr)
        return 1
    print(value)
    return 0


def _main(argv: list[str] | None = None) -> int:
    parser = _SafeArgumentParser(
        description="Agent-only AlphaInsider REST request that hides the API key."
    )
    parser.add_argument("method", nargs="?", help="HTTP method, such as GET or POST.")
    parser.add_argument("path", nargs="?", help="API path, such as /verifyToken.")
    parser.add_argument(
        "--project-root",
        metavar="PATH",
        help="Selected strategy project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--print-config",
        metavar="NAME",
        help="Print one public configured name. Only ALPHAINSIDER_STRATEGY_ID.",
    )
    parser.add_argument(
        "--query",
        action="append",
        type=_parse_key_value,
        help="Query parameter as key=value. Repeat as needed.",
    )
    body_group = parser.add_mutually_exclusive_group()
    body_group.add_argument("--json", help="Non-secret JSON request body.")
    body_group.add_argument(
        "--json-stdin",
        action="store_true",
        help="Read a JSON request body, including private values, from standard input.",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0, help="Request timeout in seconds."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the request without sending it."
    )
    args = parser.parse_args(argv)

    chosen_root = Path(args.project_root) if args.project_root else Path.cwd()
    try:
        project_root = str(_validate_project_root(chosen_root))
    except (_SetupRequestError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.print_config:
        if (
            args.method is not None
            or args.path is not None
            or args.dry_run
            or args.query
            or args.json is not None
            or args.json_stdin
        ):
            parser.error("a config lookup does not accept request arguments")
        try:
            return _print_config(args.print_config, project_root)
        except (_SetupRequestError, OSError, UnicodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if args.method is None or args.path is None:
        parser.error("a request requires METHOD PATH")

    try:
        body = _cli_body(args.json, args.json_stdin)
        if any(_is_credential_key(key) for key, _value in args.query or ()):
            raise _SetupRequestError(
                "credential query parameters are not accepted on the command line"
            )
    except _SetupRequestError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        api_key = _validated_api_key(
            _configured_value("ALPHAINSIDER_API_KEY", project_root)
        )
        prepared, prepared_body, secrets = _build_request(
            args.method,
            args.path,
            query=args.query,
            body=body,
            api_key=api_key,
        )
    except (_SetupRequestError, OSError, TypeError, UnicodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        _print_dry_run(prepared, prepared_body, secrets)
        return 0

    try:
        response = _send_request(prepared, secrets, args.timeout)
    except _SetupRequestError as exc:
        print(
            json.dumps({"success": False, "response": str(exc)}, indent=2),
            file=sys.stderr,
        )
        return 1

    print(json.dumps({"success": True, "response": response}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(_main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except Exception:  # noqa: BLE001 - credential-safe CLI boundary
        print("request failed safely", file=sys.stderr)
        raise SystemExit(1) from None
