#!/usr/bin/env python3
"""Safely create, update, or remove one value in a strategy project's .env."""

from __future__ import annotations

if __name__ != "__main__":
    raise RuntimeError(
        "set_env_value.py is CLI-only; run it from the strategy project root"
    )

import argparse
import getpass
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Sequence


ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_UNQUOTED_VALUE = re.compile(r"^[A-Za-z0-9_./:@%+=,-]+$")


class _EnvUpdateError(ValueError):
    """The requested .env update is invalid or unsafe."""


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        self.exit(
            2,
            "error: invalid arguments; pass only [--remove] and the variable name\n",
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


def _validate_project_root(project_root: Path) -> None:
    skills_root = Path(__file__).resolve().parents[2]
    resolved_root = project_root.resolve()
    if resolved_root == skills_root or skills_root in resolved_root.parents:
        raise _EnvUpdateError("refusing to write inside an installed skill directory")


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

    contents = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    replacement = _updated_contents(contents, name, value)
    existing_mode = (
        stat.S_IMODE(env_path.stat().st_mode) if env_path.exists() else 0o600
    )

    _replace_file(env_path, replacement, existing_mode)


def _remove_env(env_path: Path, name: str) -> None:
    _validate_name(name)

    if env_path.is_symlink():
        raise _EnvUpdateError("refusing to replace a symbolic-link .env")
    if not env_path.exists():
        return
    if not env_path.is_file():
        raise _EnvUpdateError(".env exists but is not a regular file")

    contents = env_path.read_text(encoding="utf-8")
    replacement = _removed_contents(contents, name)
    if replacement == contents:
        return
    _replace_file(env_path, replacement, stat.S_IMODE(env_path.stat().st_mode))


def _main(argv: Sequence[str] | None = None) -> int:
    parser = _SafeArgumentParser(
        description="Create, update, or remove one value in the project's .env."
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove the named variable without prompting for a value.",
    )
    parser.add_argument("name", help="Environment variable name to create, update, or remove.")
    args = parser.parse_args(argv)

    project_root = Path.cwd()
    env_path = project_root / ".env"
    try:
        _validate_project_root(project_root)
        _validate_name(args.name)
        if args.remove:
            _remove_env(env_path, args.name)
        else:
            if not sys.stdin.isatty():
                raise _EnvUpdateError(
                    "value entry requires an interactive terminal"
                )
            value = getpass.getpass(f"Value for {args.name}: ")
            _update_env(env_path, args.name, value)
    except (_EnvUpdateError, OSError, UnicodeError) as exc:
        parser.exit(1, f"error: {exc}\n")
    except (EOFError, KeyboardInterrupt):
        parser.exit(1, "error: no value received\n")

    action = "Removed" if args.remove else "Updated"
    print(f"{action} {args.name} in {env_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
