---
name: strategy-creator
description: Interview users one decision at a time, maintain a decision-complete plan, and build, test, backtest, document, or change one automated AlphaInsider paper-trading strategy. Use for stock or cryptocurrency strategies that may depend on market data, models, APIs, or authorized web data but send orders only to AlphaInsider.
---

# AlphaInsider Strategy Creator

Build only the project justified by a confirmed strategy plan. Keep this skill
and the sibling `alphainsider` skill read-only; they provide instructions and
helpers, not a strategy runtime.

## Scope

- Build one automated AlphaInsider paper-trading strategy per project.
- Use AlphaInsider as the only order destination; never create a live-broker
  client.
- Plan one strict `stock` or `cryptocurrency` asset class. Signals may use
  other data, but every traded instrument and target must match that class.
- Support fixed, dynamic, and constrained-dynamic instrument selection.
- Never inspect or print existing `.env` values or API keys.
- Keep generated artifacts in the selected project root. One exact confirmed
  user-level background definition is the only host-write exception.

## Start

1. Require this skill's `scripts/check_for_update.py` and
   `scripts/set_env_value.py`, plus the sibling `alphainsider` skill's
   `SKILL.md`, `scripts/alphainsider_request.py`, and
   `scripts/alphainsider_stream.py`. If any are missing, stop and show:

   ```bash
   npx skills@latest add https://github.com/AlphaInsider/skills \
     --skill alphainsider --skill strategy-creator
   ```

2. Run `scripts/check_for_update.py` once at the start of every invocation.
   Show a notice once, but never run or offer its update command. Continue
   silently if it prints nothing or cannot run.
3. Ask for the project root and recommend the invocation directory. Accept a
   normal writable user-controlled location, including beneath the user's
   home. Reject an installed skill directory, unsafe system location, or
   unusable path without elaborate denylist checks.
4. Read `references/versioning.md` to recognize an existing project without
   opening `.env`. Stop on malformed or newer versions. For a recognized
   project, ask once whether to update the existing plan or replace the
   strategy; recommend updating. Preserve unaffected decisions.
5. Before confirmation, list the exact paths and host definition the workflow
   would change. Research collisions, explain consequences, resolve overwrite
   or alternate-path choices, and record every action. Preserve unrelated
   files and select a unique identifier instead of overwriting an active
   unrelated service. Do not create backups or management metadata.

## Load references progressively

Do not preload every reference. Read each file in full only when its phase or
action begins:

- [`references/versioning.md`](references/versioning.md) — project recognition
  and upgrades. Load only selected sections from its major-version log.
- [`references/plan-template.md`](references/plan-template.md) — creating,
  replacing, or upgrading the authoritative plan.
- [`references/interview.md`](references/interview.md) — starting or resuming
  draft planning through final confirmation.
- [`references/credentials.md`](references/credentials.md) — only when a
  credential or configuration value is missing.
- [`references/background-operation.md`](references/background-operation.md) —
  the background interview phase, installation, or runtime-affecting updates.
- [`references/alphainsider-target.md`](references/alphainsider-target.md) — the
  forward-test target phase, provisioning, cleanup, or description sync.
- [`references/implementation.md`](references/implementation.md) — confirmed
  builds, replacement execution, generated docs, and maintenance.

Read the sibling `alphainsider` skill only when target or implementation work
needs its API behavior, normalized calculations, request examples, or streams.

## Plan contract

`docs/plan.md` is authoritative. Stage a replacement in
`docs/replacement-plan.md` without altering the current strategy. Plans use
only `draft`, `confirmed`, and `implemented`, and retain their
`contract_version` until `versioning.md` permits advancement.

Ask exactly one interview decision per turn, update the active plan after each
answer, and do not code while it is `draft`. Follow this order: strategy design
and resources, background operation, AlphaInsider forward-test setup,
backtesting, implementation, and final confirmation.

Complete plan confirmation is the only skill-level execution approval. It
authorizes every exact planned create, modify, overwrite, delete, stop,
disable, promotion, provisioning, ID-persistence, synchronization, build, and
background-install action. Resolve warnings and choices before confirmation;
never request another approval for a confirmed action. If any required action
or path was absent or changes afterward, return the plan to `draft`, resolve
only affected decisions, and require one new complete-plan confirmation.

Target readiness must be `ready` or `deferred`. A confirmed ready plan may
provision, build, synchronize, and install its inactive background definition.
A confirmed deferred plan permits a complete mocked local build but no remote
calls, operational commands, background installation, or `implemented` state.

## Execute the lifecycle

- **Draft:** Follow `interview.md`, loading the background, target, credential,
  and plan references only when routed. Present one normalized complete plan.
- **Confirmed:** For a ready target, follow target provisioning, then
  `implementation.md`, description synchronization, and background
  installation. For a deferred target, follow only the offline path in
  `implementation.md` and leave the plan `confirmed`.
- **Replacement:** Keep the current strategy untouched while drafting. After
  final confirmation, `implementation.md` performs only the recorded deletion,
  promotion, and build actions without another approval.
- **Implemented:** For changes, return the plan to `draft`, preserve unaffected
  decisions, interview only affected choices, and fully reconfirm before
  executing `implementation.md` maintenance.

Never start a one-cycle or continuous strategy command during build or
verification. These commands submit planned AlphaInsider paper orders without
an interactive confirmation; invoking one is the user's execution action.
