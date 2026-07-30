---
name: strategy-creator
description: Interview a user one decision at a time, plan and implement one bespoke AlphaInsider paper-trading strategy, and maintain its local workspace. Use when Codex needs to create, resume, replace, test, backtest, or document an AlphaInsider strategy using Alpaca equities or Coinbase public crypto market data.
---

# AlphaInsider Strategy Creator

Drive one strategy through `interviewing → confirmed → implemented`. Require
the sibling `$alphainsider` skill while building the workspace; the completed
workspace must run without either installed skill.

## Preflight

1. Locate this skill directory, then locate the sibling `alphainsider` skill.
   Confirm its `SKILL.md`, `scripts/runtime/`, and `references/` exist.
2. If the sibling is missing, stop before writing and tell the user to run:

   ```bash
   npx skills@latest add https://github.com/AlphaInsider/skills \
     --skill alphainsider --skill strategy-creator
   ```

3. Ask which target directory to use, recommending the current directory.
   Treat the selected directory as the workspace root; never add a wrapper.
4. Inspect the target without reading `.env`. Report every managed collision.
5. If `.alphainsider/manifest.json` exists, ask whether to resume or replace.
6. Obtain explicit consent before creating or overwriting any file. If consent
   is absent, make no changes.

On resume, preserve existing managed files and continue from `docs/plan.md`.
Creating a missing managed file or refreshing reusable machinery still needs
an explicit collision inventory and consent. On replacement, copy every
existing managed file to `.alphainsider/backups/<UTC timestamp>/`, preserving
relative paths, before writing anything. Use a unique timestamp directory and
abort without writes if backup creation fails. Never read, copy, overwrite, or
back up `.env`. Preserve every unrelated file.

## Bootstrap the workspace

After consent, create or refresh the reusable workspace machinery:

- Copy AlphaInsider `scripts/runtime/client.py` and `stream.py` into
  `strategy/clients/` as `alphainsider.py` and `alphainsider_stream.py`;
  adjust the stream's relative client import.
- Copy `scripts/market_data/alpaca.py` and `coinbase.py` from this skill into
  `strategy/clients/`; adjust relative imports.
- Copy this skill's `scripts/strategy_runtime/` into `strategy/runtime/`.
- Generate `strategy/__init__.py`, `.env.example`, `pyproject.toml`,
  `AGENTS.md`, and `CONTEXT.md` directly in the target.
- Merge required ignore entries without replacing unrelated `.gitignore`
  content: `.env`, `.alphainsider/`, `docs/plan.md`, `strategy/`, and `tests/`.
- Write `.alphainsider/manifest.json` with schema version `1`, the selected
  target, and the exact managed paths. Store checkpoints under
  `.alphainsider/state/`. Create `.alphainsider/backups/` and initialize
  `.alphainsider/state/checkpoint.json` to `{ "last_event_id": null }` for a
  fresh workspace. Write generated files through same-directory temporary
  files and atomic replacement; if generation fails, keep the prior files.

The generated project requires Python 3.11+ with `httpx`, `python-dotenv`,
`alpaca-py`, and `websockets`; its dev dependencies are `pytest` and
`pytest-asyncio`.

## Lifecycle

Read `docs/plan.md` when it exists. Missing or invalid state means
`interviewing`; valid states are `interviewing`, `confirmed`, and
`implemented`.

### Interviewing

- Discover workspace and API facts before asking the user.
- Ask exactly one decision question per turn. Recommend an answer with a
  short rationale, but record only the user's answer.
- Treat required fields as unresolved even if the user calls an incomplete
  description a complete plan. Never invent a default or defer a required
  interview answer to generated configuration; ask for the next missing
  decision instead.
- On the first confirmed answer, copy `references/plan-template.md` to
  `docs/plan.md`. Persist every later confirmed answer immediately.
- Resolve all dependencies and contradictions before requesting confirmation.

Cover at least:

1. Exactly one primary provider: Alpaca equities or Coinbase public crypto.
2. Provider symbols/product IDs and matching AlphaInsider `stock_id` values.
3. Deterministic or LLM signal logic, including holding or exit timing.
4. Polling interval/timeframe or WebSocket channels.
5. Fixed normalized orders or allocation rebalancing and sizing.
6. Position, stop, drawdown, kill-switch, and open-order constraints.
7. Market-hours, continuous, or custom schedule.
8. Backtesting only when every input is historically reconstructable without
   lookahead. If replayable, ask whether the user wants signal replay, then
   ask for its window. If not replayable, record why and do not offer it.

When all sections are resolved, present the complete plan. Do not generate
bespoke strategy logic until the user explicitly confirms it. Then set
`status: confirmed`.

### Confirmed

Before implementation, read in full:

- This skill's `references/alpaca.md` or `references/coinbase.md` for the
  selected provider.
- The sibling AlphaInsider skill's `references/input-multiplier.md`,
  `references/trades.md`, and `references/websockets.md` as relevant.

Generate:

- `strategy/decision.py`: pure decision logic with injected data and clients.
- `strategy/loop.py`: reconcile → fetch → decide → submit paper orders.
- `strategy/__main__.py`: `run-once` and `run` commands.
- `strategy/backtest.py`: only when the user accepted signal replay.
- `tests/`: offline tests for clients, runtime, decisions, and orchestration.

Mandatory runtime behavior:

- AlphaInsider is the only order destination and all orders are paper orders.
- Reconcile current positions and open orders before every decision.
- Never assume a missing `input_multiplier` is `1`.
- Use `EventCheckpoint` to reject duplicate market events across restarts.
- Use `StrategyRunner` for graceful shutdown and bounded retry/backoff.
- Never instantiate an Alpaca trading client.
- Never call Coinbase accounts, orders, or authenticated user channels.

Backtests are signal-only and read-only. Replay production decision logic in
chronological order, expose no future information, make no AlphaInsider calls,
and do not simulate cash, fills, positions, fees, or slippage. Report signal
counts, directional hit rate, forward returns, timestamped records, and
unevaluable trailing signals. Support optional `--start` and `--end`.

Finish by creating or updating the workspace-root `README.md` with purpose,
signals, cadence, orders, schedule, risks, prerequisites, environment
variables, installation, and the exact commands. If `README.md` already
exists, include it in the collision inventory, obtain explicit overwrite
consent, and preserve unrelated content while updating the strategy guidance:

```bash
python -m strategy run-once
python -m strategy run
python -m strategy backtest  # only when selected
```

Run the complete offline suite. Automated tests must never submit paper
orders. Network smoke tests are read-only and opt-in with
`RUN_SMOKE_TESTS=1 pytest -m smoke`. Once code, tests, and documentation agree,
update `CONTEXT.md`, add strategy-specific ADRs under `docs/adr/` only for
durable trade-offs, and set `status: implemented`.

### Implemented

For maintenance, keep `docs/plan.md`, `strategy/`, tests, `CONTEXT.md`, and
`README.md` synchronized. Re-read the selected provider reference and the
canonical AlphaInsider references before changing integration behavior.
