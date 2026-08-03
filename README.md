# AlphaInsider Skills

Official agent skills for building with AlphaInsider and creating standalone
AlphaInsider paper-trading strategies.

## Skills

- `alphainsider` — API references, credential-safe request tooling, normalized
  sizing guidance, and reusable REST/WebSocket clients.
- `strategy-creator` — a knowledge-only manual that interviews one decision at
  a time, researches an appropriate data/tool stack, maintains a confirmed
  plan, and builds, tests, documents, or changes one automated stock or
  cryptocurrency strategy.

## Install

AlphaInsider API skill only:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider
```

Strategy Creator and its required dependency:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider \
  --skill strategy-creator
```

## Strategy Creator workflow

Strategy Creator requires the AlphaInsider skill at startup, asks for a project
root, and records each interview decision in `docs/plan.md`. It challenges
unreliable assumptions, researches current providers and libraries, and
prefers Alpaca for equity data or Coinbase for cryptocurrency data when they
fit the confirmed requirements. Other supported data sources and explicitly
authorized scraping remain available when justified.

Each project retains the configured AlphaInsider strategy's strict stock or
cryptocurrency type. Its instruments may be fixed, selected dynamically at
runtime, or selected dynamically within a confirmed constraint. Explicitly
named instruments are verified during planning; runtime-selected candidates
are resolved and type-checked through AlphaInsider before they can be traded.

The plan progresses through `draft`, `confirmed`, and `implemented`.
Confirmation authorizes the agent to build a small standalone project with
strategy source, offline tests, dependency configuration, `.env.example`,
`README.md`, and `AGENTS.md`. The generated project uses AlphaInsider as its
only paper-order destination and obtains its configured strategy from `.env`.
Only credentials and local/cache/build artifacts are ignored; the plan, code,
tests, and documentation remain commit-ready.

Backtesting is optional and offered only when the strategy's historical inputs
can be reconstructed without lookahead. Generated projects expose one-cycle
and continuous operation plus tests and, when selected, a backtest command.
Automated verification never submits AlphaInsider orders.

This version does not recognize or migrate workspaces created by the previous
runtime-generating Strategy Creator.

Strategy Creator treats its own directory and the AlphaInsider skill directory
as read-only. It writes generated artifacts only into the user-selected project
folder, defaulting to the invocation directory when that is a reasonable
user-controlled location. Project folders beneath a user's home are allowed;
installed skill directories and obviously unsafe system locations are not.
Persisted project paths remain relative and portable.

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
