#!/usr/bin/env python3
"""Safely create, update, or remove one value in a strategy project's .env."""

from __future__ import annotations

if __name__ != "__main__":
    raise RuntimeError("set_env_value.py is CLI-only; do not import it")

import argparse
import getpass
import json
import os
import re
import stat
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path


ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_UNQUOTED_VALUE = re.compile(r"^[A-Za-z0-9_./:@%+=,-]+$")
_MAX_VALUE_BYTES = 16 * 1024
_MAX_ENV_BYTES = 1024 * 1024


class _EnvUpdateError(ValueError):
    """The requested .env update is invalid or unsafe."""


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        self.exit(
            2,
            "error: invalid arguments; pass NAME and provide its value through "
            "protected standard input, or pass --remove NAME\n",
        )


def _validate_name(name: str) -> None:
    if not ENV_NAME.fullmatch(name):
        raise _EnvUpdateError(
            "variable name must start with a letter or underscore and contain "
            "only letters, numbers, and underscores"
        )


def _validate_value(value: str) -> None:
    if not value:
        raise _EnvUpdateError("value must not be empty")
    if "\n" in value or "\r" in value:
        raise _EnvUpdateError("value must be a single line")


def _read_value() -> str:
    if sys.stdin.isatty():
        value = getpass.getpass("Value: ")
    else:
        encoded = sys.stdin.buffer.read(_MAX_VALUE_BYTES + 1)
        if len(encoded) > _MAX_VALUE_BYTES:
            raise _EnvUpdateError("value is too large")
        try:
            value = encoded.decode("utf-8")
        except UnicodeDecodeError:
            raise _EnvUpdateError("value must be UTF-8") from None
        if value.endswith("\n"):
            value = value[:-1]
            value = value.removesuffix("\r")
    _validate_value(value)
    return value


def _validate_project_root(project_root: Path) -> Path:
    resolved_root = project_root.expanduser().resolve()
    if not resolved_root.is_dir():
        raise _EnvUpdateError("project root must be an existing directory")
    skills_root = Path(__file__).resolve().parents[2]
    if resolved_root == skills_root or skills_root in resolved_root.parents:
        raise _EnvUpdateError("refusing to write inside an installed skill directory")
    if not (resolved_root / "plan.md").is_file():
        raise _EnvUpdateError("project root must contain plan.md")
    return resolved_root


def _render_assignment(name: str, value: str) -> str:
    rendered_value = (
        value
        if _UNQUOTED_VALUE.fullmatch(value)
        else json.dumps(value, ensure_ascii=False)
    )
    return f"{name}={rendered_value}\n"


def _updated_contents(contents: str, name: str, value: str) -> str:
    assignment = _render_assignment(name, value)
    definition = re.compile(rf"^\s*(?:export\s+)?{re.escape(name)}\s*=")
    output: list[str] = []
    replaced = False

    for line in contents.splitlines(keepends=True):
        if definition.match(line):
            if not replaced:
                output.append(assignment)
                replaced = True
            continue
        output.append(line)

    if not replaced:
        if output and not output[-1].endswith(("\n", "\r")):
            output[-1] = f"{output[-1]}\n"
        output.append(assignment)

    return "".join(output)


def _removed_contents(contents: str, name: str) -> str:
    definition = re.compile(rf"^\s*(?:export\s+)?{re.escape(name)}\s*=")
    return "".join(
        line
        for line in contents.splitlines(keepends=True)
        if not definition.match(line)
    )


def _replace_file(env_path: Path, replacement: str, mode: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=env_path.parent, prefix=".env.", text=True
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(replacement)
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, env_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _update_env(env_path: Path, name: str, value: str) -> None:
    _validate_name(name)
    _validate_value(value)

    if env_path.is_symlink():
        raise _EnvUpdateError("refusing to replace a symbolic-link .env")
    if env_path.exists() and not env_path.is_file():
        raise _EnvUpdateError(".env exists but is not a regular file")

    if env_path.exists() and env_path.stat().st_size > _MAX_ENV_BYTES:
        raise _EnvUpdateError(".env is too large to update safely")
    contents = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    replacement = _updated_contents(contents, name, value)
    _replace_file(env_path, replacement, 0o600)


def _remove_env(env_path: Path, name: str) -> None:
    _validate_name(name)

    if env_path.is_symlink():
        raise _EnvUpdateError("refusing to replace a symbolic-link .env")
    if not env_path.exists():
        return
    if not env_path.is_file():
        raise _EnvUpdateError(".env exists but is not a regular file")

    if env_path.stat().st_size > _MAX_ENV_BYTES:
        raise _EnvUpdateError(".env is too large to update safely")
    contents = env_path.read_text(encoding="utf-8")
    replacement = _removed_contents(contents, name)
    if replacement == contents:
        if stat.S_IMODE(env_path.stat().st_mode) != 0o600:
            os.chmod(env_path, 0o600)
        return
    _replace_file(env_path, replacement, 0o600)


def _main(argv: Sequence[str] | None = None) -> int:
    parser = _SafeArgumentParser(
        description="Agent-only update or removal of one project .env value."
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove the named variable without receiving a value.",
    )
    parser.add_argument(
        "--project-root",
        metavar="PATH",
        help="Selected strategy project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "name", help="Environment variable name to create, update, or remove."
    )
    args = parser.parse_args(argv)

    chosen_root = Path(args.project_root) if args.project_root else Path.cwd()
    try:
        project_root = _validate_project_root(chosen_root)
        env_path = project_root / ".env"
        if args.remove:
            _remove_env(env_path, args.name)
        else:
            _update_env(env_path, args.name, _read_value())
    except (_EnvUpdateError, OSError, UnicodeError) as exc:
        parser.exit(1, f"error: {exc}\n")

    action = "Removed" if args.remove else "Updated"
    print(f"{action} {args.name} in {env_path.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(_main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except Exception:  # noqa: BLE001 - secret-safe CLI boundary
        print("error: environment update failed safely", file=sys.stderr)
        raise SystemExit(1) from None
