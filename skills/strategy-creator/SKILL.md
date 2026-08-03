---
name: strategy-creator
description: Interview users one decision at a time, maintain a decision-complete plan, and build, test, backtest, document, or change one automated AlphaInsider paper-trading strategy. Use for stock or cryptocurrency strategies that may depend on market data, models, APIs, or authorized web data but send orders only to AlphaInsider.
---

# AlphaInsider Strategy Creator

Use this skill as an instruction manual. Build only the project justified by the
confirmed strategy plan; this skill contains no provider or runtime code.

## Scope

- Build one fully automated AlphaInsider paper-trading strategy per project.
- Fix the project to the configured AlphaInsider strategy's explicit asset
  class: `stock` or `cryptocurrency`. Every traded instrument must match that
  class. Cross-asset and alternative data may inform signals but cannot expand
  it.
- Support fixed, dynamic, and constrained-dynamic instrument selection. Do not
  require a predefined instrument list when the strategy selects candidates at
  runtime.
- Use AlphaInsider as the only order destination. Never instantiate a live
  broker trading client.
- Map the project to the user's AlphaInsider strategy through
  `ALPHAINSIDER_STRATEGY_ID` in `.env`.
- Never inspect, print, request, or copy `.env` values or API keys.
- Treat this skill directory and the sibling `alphainsider` skill directory as
  read-only sources. Never create, edit, format, or delete files in either one
  while planning, building, testing, or maintaining a user's strategy.
- Write every generated strategy artifact inside the selected project root.

## Preflight

1. Locate this skill and the sibling `alphainsider` skill. Require its
   `SKILL.md`, `scripts/alphainsider_request.py`, and `scripts/runtime/` before
   doing any work. If missing, stop and ask the user to install both skills:

   ```bash
   npx skills@latest add https://github.com/AlphaInsider/skills \
     --skill alphainsider --skill strategy-creator
   ```

2. Read [references/interview.md](references/interview.md) and
   [references/plan-template.md](references/plan-template.md) in full.
3. Ask for the project root, recommending the directory from which the user
   invoked the skill. Accept a normal user-controlled project location,
   including a suitable project directory beneath the user's home, when the
   required files can be added safely. Reject an installed skill directory, an
   obviously unsafe system location, or a location where the project cannot be
   created. Use reasonable judgment; do not maintain an exhaustive path
   denylist or perform elaborate filesystem checks. If unsuitable, explain why
   and ask for another path.
4. Inspect the selected project root without opening `.env`; list only files
   this workflow would create or change that already exist.
5. Treat an existing current-format `docs/plan.md` as resumable. Treat every
   other collision as an ordinary file conflict and obtain explicit overwrite
   approval. Preserve unrelated files.

Do not recognize or migrate legacy manifests, checkpoints, backups, generated
runtime layouts, provider modules, or plan schemas. Do not create replacement
backups or management metadata.

## Plan lifecycle

Use `docs/plan.md` as the source of truth. Its only states are `draft`,
`confirmed`, and `implemented`.

### Draft

1. On the first confirmed interview answer, create `docs/plan.md` from the
   plan template after obtaining permission to create or replace that path.
2. Follow the interview reference. Ask exactly one decision question per turn,
   recommend an answer with a short reason, wait for the response, and write
   the normalized answer immediately. Do not preserve the transcript.
3. Research discoverable facts instead of asking the user. When requirements
   are known, research current data sources and libraries using primary
   documentation. Recommend the smallest feasible stack and obtain the user's
   confirmation before recording it.
4. Prefer Alpaca for equities and Coinbase for cryptocurrency when they meet
   the requirements. Treat scraping as an explicitly approved, authorized
   fallback when a supported API or feed is unsuitable.
5. Prefer deterministic signal logic. Permit hosted models only when the plan
   defines their inputs, outputs, version expectations, cost limits, timeouts,
   failure behavior, and replay limitations.
6. Before confirmation, use the sibling skill's request helper for read-only
   validation of the configured AlphaInsider strategy and its asset class. If
   the user explicitly names instruments, also validate their AlphaInsider
   mappings. For dynamic selection, record the runtime resolution contract
   without requiring candidate mappings in advance. Let the helper read
   `.env`; never read it yourself. Record validation results without
   credentials or strategy IDs.
7. Offer backtesting only when every decision input can be reconstructed as it
   was known at the decision time. If feasible, ask whether the user wants it;
   if accepted, resolve the window and scope. Otherwise record why it would be
   misleading or infeasible.
8. Resolve contradictions and implementation-blocking decisions, then present
   the complete normalized plan. Explicit confirmation changes the status to
   `confirmed` and authorizes implementation immediately.

Do not generate strategy code while the plan is `draft`. Conservative agent
defaults are allowed for incidental mechanics only when labeled in the plan;
the final confirmation must make them visible and accepted.

### Confirmed

Read the relevant sibling AlphaInsider references before writing integration
code, especially authentication, runtime-client, stocks, trades,
input-multiplier, and WebSocket guidance as applicable.

Before writing, inventory every exact project path the confirmed plan will
create or change. Plan confirmation authorizes new files, but an existing file
still requires explicit overwrite approval. Keep every write inside the
selected project root. Use machine-specific absolute paths only to locate the
project during the current run; persist project-relative paths in the project.

Build the smallest standalone project that satisfies the plan:

- Use Python by default. Use another language only when the plan records a
  concrete ecosystem reason and an equivalent AlphaInsider integration.
- Create `strategy/`, `tests/`, `.env.example`, ecosystem dependency
  configuration, `.gitignore`, `README.md`, and `AGENTS.md`. Keep internal
  modules specific to the strategy instead of imposing a generic framework.
- For Python, read the sibling `scripts/runtime/client.py` as an immutable
  source and copy it into the project; copy `stream.py` only when WebSockets are
  required. Preserve credential and normalized-value behavior and adjust the
  project copies without modifying or duplicating clients in either skill.
- Put only variable names and safe examples in `.env.example`. Keep `.env`,
  credentials, caches, and build artifacts ignored; keep the plan, source,
  tests, and documentation commit-ready.
- Expose project-native commands for one decision cycle, continuous operation,
  tests, and an optional backtest when selected. Do not add a dry-run mode.
- Implement the plan's `fixed`, `dynamic`, or `constrained dynamic` instrument
  selection mode. For each actionable runtime candidate that lacks an exact
  AlphaInsider ID, use `search_stocks` and reject missing or ambiguous matches;
  never guess a mapping. Validate resolved IDs with `get_stocks`, batching
  candidates when practical, and require each returned `security` to equal the
  configured strategy's `stock` or `cryptocurrency` type before ordering.
- Never submit an order for an unvalidated, missing, ambiguous, or mismatched
  instrument. Revalidate newly selected or changed candidates according to the
  plan's freshness rule. On validation failure, follow the plan-specific choice
  to continue with valid candidates or abort that decision cycle.
- Reconcile relevant AlphaInsider positions and open orders before decisions,
  validate the configured strategy type at startup, and implement the plan's
  stale-data, retry, duplicate-event, recovery, logging, sizing, and risk
  behavior. Never treat a missing `input_multiplier` as `1`.
- Keep decision logic independently testable. When backtesting is selected,
  replay production decisions chronologically without AlphaInsider calls or
  future information. For dynamic selection, reconstruct the historical
  candidate set as it existed at each decision time without survivorship bias.
  Add portfolio accounting only when its execution and cost assumptions are
  credible and documented.

After implementation, create strategy-specific offline tests for signals,
risk rules, order mapping, orchestration, and backtesting when selected. Mock
all external services. Tests and implementation verification must never submit
AlphaInsider orders; do not run an order-submitting command merely to verify
the build.

Write `README.md` for humans: purpose, behavior, prerequisites, setup,
environment variable names, commands, monitoring, limitations, and recovery.
Write `AGENTS.md` for agents: treat `docs/plan.md` as authoritative, preserve
the credential boundary, identify code/test entry points, and require the
maintenance workflow below.

Run the complete offline suite and static checks. When code, tests, plan, and
documentation agree, set the plan status to `implemented`. Deployment or
hosting is outside this workflow unless the user separately requests it.
Before handoff, confirm that every created or changed strategy path belongs to
the selected project root and that no operation wrote to either skill
directory.

### Implemented

For any behavior change, return the plan to `draft`, interview the affected
decisions one at a time, and obtain confirmation before editing code. Then
update implementation, tests, `README.md`, and `AGENTS.md` together and restore
`implemented` only after verification passes.
