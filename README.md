# AlphaInsider Skills

Official agent skills for building with AlphaInsider and creating standalone
AlphaInsider paper-trading strategies.

## Skills

- `alphainsider` — API references, credential-safe request tooling, normalized
  sizing guidance, and reusable REST/WebSocket clients.
- `strategy-creator` — an instruction manual with one local `.env` setup helper
  that interviews one decision at a time, researches an appropriate data/tool
  stack, maintains a confirmed plan, and builds, tests, documents, or changes
  one automated stock or cryptocurrency strategy.

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

When `docs/plan.md` has a valid lifecycle status, the `# Strategy Plan` title,
and the current template sections, Strategy Creator recognizes the folder as
an existing project. It first asks whether to update the existing plan or
replace the trading strategy with a new one, recommending an update to preserve
unaffected decisions.

A replacement is planned separately in `docs/replacement-plan.md`, leaving the
current plan and implementation untouched. Confirming the replacement plan
does not authorize deletion or implementation. The agent then lists every old
generated project path proposed for deletion and obtains separate explicit
approval. Approval promotes the replacement plan to `docs/plan.md`, removes
only the approved old artifacts, and starts re-implementation. The workflow
never recursively deletes the project root and never deletes `.env`,
credentials, caches, unrelated files, or files with uncertain ownership. If
approval is declined, the working strategy remains unchanged and the confirmed
replacement plan remains resumable.

The interview asks one short question at a time in plain trading language. To
define how results will be judged, it proposes an understandable review period,
results after fees, and loss or behavior that would mean the strategy needs to
change or stop. The user can accept or adjust each recommendation without
having to supply formal planning terms or design performance measurements from
scratch.

If a required environment variable is missing, Strategy Creator names it and
the exact project `.env` path, then asks the user either to add it there or to
paste it in chat with a warning that chat is less secure. A pasted value is
written through Strategy Creator's non-echoing helper, never displayed or
recorded in project artifacts, and followed by non-ordering validation. The
helper updates only the named entry, preserves unrelated `.env` content, and
never writes inside an installed skill directory.

Each project retains the configured AlphaInsider strategy's strict stock or
cryptocurrency type. Its instruments may be fixed, selected dynamically at
runtime, or selected dynamically within a confirmed constraint. Explicitly
named instruments are verified during planning; runtime-selected candidates
are resolved and type-checked through AlphaInsider before they can be traded.

The plan progresses through `draft`, `confirmed`, and `implemented`.
Confirmation of the active `docs/plan.md` authorizes the agent to build a small
standalone project with strategy source, offline tests, dependency
configuration, `.env.example`, `README.md`, and `AGENTS.md`. The generated
project uses AlphaInsider as its only paper-order destination and obtains its
configured strategy from `.env`. Only credentials and local/cache/build
artifacts are ignored; the plan, code, tests, and documentation remain
commit-ready.

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
