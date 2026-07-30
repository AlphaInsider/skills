# AlphaInsider Skills

Official agent skills for building with AlphaInsider and creating standalone
AlphaInsider paper-trading strategies.

## Skills

- `alphainsider` — API references, credential-safe request tooling, normalized
  sizing guidance, and reusable REST/WebSocket clients.
- `strategy-creator` — a one-question-at-a-time interview that plans, builds,
  tests, and documents one standalone strategy using Alpaca equities or
  Coinbase public crypto market data.

## Install

AlphaInsider API skill only:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider
```

Strategy Creator and its required build-time dependency:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider \
  --skill strategy-creator
```

The Strategy Creator asks for a target directory, defaults to the current
directory, obtains explicit consent before overwriting, and generates a flat
workspace with `docs/`, `strategy/`, and `tests/`. The finished strategy runs
without either installed skill.

## Generated workspace

The selected target is the workspace root; Strategy Creator never adds a
wrapper directory. Managed state and backups stay under `.alphainsider/`, the
confirmed plan lives at `docs/plan.md`, and executable code lives in
`strategy/`. Existing managed workspaces can be resumed or replaced. A
replacement backs up managed files first, preserves unrelated files, and
never reads, overwrites, or backs up `.env`.

After implementation, the standalone workspace supports:

```bash
python -m strategy run-once
python -m strategy run
python -m strategy backtest  # only when selected during planning
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm ci
python scripts/validate_catalog.py
pytest
npm run skills:list
```
