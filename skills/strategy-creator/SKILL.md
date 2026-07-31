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
4. Inspect the target without reading `.env`. Report every managed collision,
   including both candidate provider clients (`strategy/clients/alpaca.py` and
   `strategy/clients/coinbase.py`), even though only the selected provider's
   file is ever written.
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
- Copy only provider-neutral machinery here. The single market-data provider
  client is copied in the Confirmed phase, after `docs/plan.md` records the
  provider decision.
- Copy this skill's `scripts/strategy_runtime/` into `strategy/runtime/`.
- Generate `strategy/__init__.py`, `strategy/clients/__init__.py`,
  `.env.example`, `pyproject.toml`, `AGENTS.md`, and `CONTEXT.md` directly in
  the target. `.env.example` starts with exactly the provider-neutral
  variables `ALPHAINSIDER_API_KEY=` and `ALPHAINSIDER_STRATEGY_ID=`; provider
  variables are appended in the Confirmed phase.
- Merge secret and local-artifact entries into `.gitignore` without replacing
  unrelated content: `.env`, virtual environments, Python caches, test caches,
  build output, and OS/IDE files. Never ignore `.alphainsider/`, `docs/`,
  `strategy/`, `tests/`, `.env.example`, or another generated project file,
  and never add a nested ignore file that excludes them.
- Write `.alphainsider/manifest.json` with schema version `1`, target `.` so
  the project remains portable, and the exact workspace-relative managed
  paths, including `.gitignore`. Store checkpoints under
  `.alphainsider/state/`. Create `.alphainsider/backups/` and initialize
  `.alphainsider/state/checkpoint.json` to `{ "last_event_id": null }` for a
  fresh workspace. Write generated files through same-directory temporary
  files and atomic replacement; if generation fails, keep the prior files.
  When the Confirmed phase copies the provider client, append its
  workspace-relative path to the manifest under the same atomic-write rules.

Keep every tracked file portable: use workspace-relative paths and never write
the user's home directory, the target's absolute path, credentials, or `.env`
values into generated code, configuration, metadata, or documentation.

The generated project requires Python 3.11+ with `httpx>=0.27`,
`python-dotenv>=1.0`, and `websockets>=12`; its dev dependencies are
`pytest>=8` and `pytest-asyncio>=0.23`. Provider clients must call documented
REST and WebSocket protocols directly; never add an Alpaca or Coinbase SDK.

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
   Use the sibling skill's read-only `getStocks` workflow to snapshot each
   asset's `security`, `peg`, `fee`, `slippage`, and UTC retrieval time.
   Reject any instrument whose `security` does not match the selected
   provider's class — `stock` for Alpaca, `cryptocurrency` for Coinbase —
   and resolve the mismatch before recording the universe.
3. Deterministic or LLM signal logic, including holding or exit timing.
4. Polling endpoint/interval/timeframe or WebSocket channels. For Alpaca,
   record feed, adjustment, `asof`, late-bar, halt, and reconnect behavior.
   For Coinbase, record granularity, heartbeat, sequence-gap detection, and
   state-resynchronization behavior. Batch all selected instruments and
   channels onto one provider/feed connection by default; split connections
   only for a documented provider limit or measured throughput need.
5. Fixed normalized orders or allocation rebalancing and sizing.
6. Position, stop, drawdown, kill-switch, and open-order constraints.
7. Market-hours, continuous, or custom schedule.
8. Backtesting only when every input is historically reconstructable without
   lookahead. If replayable, ask whether the user wants signal replay, then
   ask for its window. For accepted USD-pegged universes, next ask for a
   positive default starting value in USD and follow `references/backtesting.md`.
   Keep non-USD replays signal-only. If not replayable, record why and do not
   offer it.

When all sections are resolved, present the complete plan. Do not generate
bespoke strategy logic until the user explicitly confirms it. Then set
`status: confirmed`.

### Confirmed

Before implementation, read in full:

- This skill's `references/alpaca.md` or `references/coinbase.md` for the
  selected provider.
- This skill's `references/backtesting.md` when the user accepted replay.
- The sibling AlphaInsider skill's `references/input-multiplier.md`,
  `references/stocks.md`, `references/trades.md`, `references/webhooks.md`, and
  `references/websockets.md` as relevant.

Then copy the selected provider's client — and only that one — from this
skill's `scripts/market_data/alpaca.py` or `scripts/market_data/coinbase.py`
into `strategy/clients/` under the same filename; the file is self-contained.
Never copy, import, or reference the other provider's client anywhere in the
workspace. Append the new path to `.alphainsider/manifest.json`. If a file
already exists at that path, apply the resume rules: collision inventory and
explicit consent. For Alpaca strategies, also append `ALPACA_KEY=`,
`ALPACA_SECRET=`, and `ALPACA_FEED=iex` to `.env.example`; Coinbase strategies
add no variables.

Generate:

- `strategy/decision.py`: pure decision logic with injected data and clients.
- `strategy/loop.py`: reconcile → fetch → decide → submit paper orders.
- `strategy/__main__.py`: `run-once` and `run` commands; both validate the
  AlphaInsider strategy type at startup.
- `strategy/backtest.py`: only when the user accepted signal replay.
- `tests/`: offline tests for clients, runtime, decisions, orchestration, and
  backtest accounting when selected.

Mandatory runtime behavior:

- AlphaInsider is the only order destination and all orders are paper orders.
- Before `run` or `run-once` starts its first decision cycle, call
  `ensure_strategy_type(client, "stock")` in an Alpaca workspace or
  `ensure_strategy_type(client, "cryptocurrency")` in a Coinbase workspace,
  and refuse to run on `StrategyTypeMismatchError`. Backtests make no
  AlphaInsider calls and never run this check.
- Reconcile current positions and open orders before every decision.
- Never assume a missing `input_multiplier` is `1`.
- Use `EventCheckpoint` to reject duplicate market events across restarts.
- Use `StrategyRunner` for graceful shutdown and bounded retry/backoff.
- Never instantiate an Alpaca trading client.
- Never call Coinbase accounts, orders, or authenticated user channels.

Backtests are read-only. Replay production decision logic chronologically,
expose no future information, and make no AlphaInsider calls during replay.
For every accepted USD portfolio replay, implement the cash, position, cost,
valuation, reporting, CLI, and test contract in `references/backtesting.md`.
Keep accepted non-USD replays signal-only and explain the limitation.

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

For portfolio-valued backtests, document the planned default and the optional
`--initial-value` override.

Run the complete offline suite. Automated tests must never submit paper
orders. Network smoke tests are read-only and opt-in with
`RUN_SMOKE_TESTS=1 pytest -m smoke`. Once code, tests, and documentation agree,
update `CONTEXT.md`, add strategy-specific ADRs under `docs/adr/` only for
durable trade-offs, and set `status: implemented`.

Before handoff, verify the generated project is ready for version control. If
the target is in a Git worktree, use `git check-ignore -v` and `git status` to
confirm `.alphainsider/`, `docs/`, `strategy/`, `tests/`, `.env.example`,
`pyproject.toml`, `README.md`, `AGENTS.md`, and `CONTEXT.md` are eligible to be
committed. Only secrets and local/cache/build artifacts may remain ignored.
Resolve target `.gitignore` conflicts within the granted consent and report
any inherited or global ignore rule rather than editing files outside the
selected workspace. Do not initialize Git, commit, configure a remote, or push
unless the user separately asks.

### Implemented

For maintenance, keep `.alphainsider/`, `.gitignore`, `docs/plan.md`,
`strategy/`, tests, `CONTEXT.md`, and `README.md` synchronized and
version-control-ready. Re-read the selected provider reference and the
canonical AlphaInsider references before changing integration behavior.
