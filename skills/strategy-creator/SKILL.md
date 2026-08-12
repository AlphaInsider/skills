---
name: strategy-creator
description: Interview users one decision at a time, maintain a decision-complete plan, and build, test, backtest, document, change, replace, retire, or clean up one automated AlphaInsider paper-trading strategy. Use for stock or cryptocurrency strategies that may depend on market data, models, APIs, or authorized web data but send orders only to AlphaInsider.
---

# AlphaInsider Strategy Creator

Build only the project justified by a confirmed strategy plan. Keep this skill
and the sibling `alphainsider` skill read-only.

## Scope

- Build one automated strategy per project, send paper orders only to
  AlphaInsider, and never create a live-broker client.
- Plan one strict `stock` or `cryptocurrency` asset class and fixed, dynamic,
  or constrained-dynamic selection. Every traded instrument and target must
  match that class.
- Never inspect or print existing `.env` values or API keys.
- Keep generated artifacts in the selected project root. Exact confirmed
  user-level native operation definitions are the only host-write exception;
  confirmed agent scheduled tasks are external managed resources.

## Start

1. Require this skill's two scripts and the sibling `alphainsider` skill and
   its two scripts. If any are missing, stop and show:

   ```bash
   npx skills@latest add https://github.com/AlphaInsider/skills \
     --skill alphainsider --skill strategy-creator
   ```

2. Run `scripts/check_for_update.py` once per invocation. Show its notice once,
   never run or offer its update command, and continue on no output or failure.
3. Ask for the project root and recommend the invocation directory. Accept a
   normal writable user-controlled location, including beneath the user's
   home. Reject an installed skill directory, unsafe system location, or
   unusable path without elaborate denylist checks.
4. Read `references/versioning.md` to recognize an existing project without
   opening `.env`. Stop on malformed or newer versions. For a recognized
   project, ask once whether to update, replace, or retire the strategy;
   recommend updating. Preserve unaffected decisions. Resume a cleanup only
   for an explicit cleanup request.
5. Before confirmation, inventory every changed project path, native
   definition, and agent task. Research collisions, explain consequences,
   resolve overwrite or alternate-identity choices, and record every action.
   Preserve unrelated resources, never overwrite an active unrelated runner,
   and create no metadata beyond the documented lifecycle plans.

## Load references progressively

Do not preload every reference. Read each file in full only when its phase or
action begins:

- [`references/versioning.md`](references/versioning.md) — recognition and
  upgrades; load only selected version-log sections.
- [`references/plan-template.md`](references/plan-template.md) — active plans.
- [`references/interview.md`](references/interview.md) — draft through final
  confirmation.
- [`references/credentials.md`](references/credentials.md) — missing values.
- [`references/cleanup-plan-template.md`](references/cleanup-plan-template.md)
  — staging one exact retirement or outgoing replacement cleanup.
- [`references/cleanup.md`](references/cleanup.md) — explicit retirement,
  replacement cleanup, pending-cleanup recovery, or remote deletion.
- [`references/operation-and-scheduling.md`](references/operation-and-scheduling.md)
  — the operation interview phase, installation, scheduling, or
  runtime-affecting updates.
- [`references/alphainsider-target.md`](references/alphainsider-target.md) — the
  forward-test target phase, provisioning, cleanup, or description sync.
- [`references/implementation.md`](references/implementation.md) — confirmed
  execution and maintenance.

Read the sibling `alphainsider` skill only for needed API behavior.

## Plan contract

`docs/plan.md` is authoritative. Stage a replacement in
`docs/replacement-plan.md` without altering the current strategy. Active plans
use `draft`, `confirmed`, or `implemented`; completed retirement uses
`retired`. Stage one explicit cleanup in `docs/cleanup-plan.md`, which uses
only `draft` or `confirmed`. Retain `contract_version` until `versioning.md`
permits advancement.

Ask exactly one interview decision per turn, update the active plan after each
answer, and do not code while it is `draft`. Follow this order: objective,
market and instruments, strategy behavior, data and resources, execution and
risk, backtesting, implementation contract, operation and scheduling,
AlphaInsider forward-test setup, and final confirmation.

Complete plan confirmation is the only skill-level execution approval. It
authorizes every exact planned create, modify, overwrite, delete, stop, pause,
disable, activation, promotion, provisioning, ID-persistence, synchronization,
build, native-operation, and agent-task action. Resolve warnings and choices
before confirmation; never request another approval for a confirmed action. If
any required action, identity, or path was absent or changes afterward, return
the plan to `draft`, resolve only affected decisions, and require one new
complete-plan confirmation.

Cleanup is a post-creation lifecycle, not an interview phase. Only its plan may
contain the exact non-secret strategy ID. One final cleanup confirmation, or a
replacement's joint confirmation, authorizes its attributable actions.

Target readiness must be `ready` or `deferred`. A confirmed ready plan may
provision, build, synchronize, and install or schedule its exact operation
resources in the confirmed active or inactive state without an immediate run.
A confirmed deferred plan permits a complete mocked local build but no remote
calls, operational commands, managed resources, or `implemented` state.

## Execute the lifecycle

- **Draft:** Follow `interview.md` and present one normalized complete plan.
- **Confirmed:** For a ready target, follow target provisioning, then
  `implementation.md`, description synchronization, and operation-resource
  installation or scheduling. For a deferred target, follow only the offline path in
  `implementation.md` and leave the plan `confirmed`.
- **Replacement:** Keep the current strategy untouched while drafting. After
  joint final confirmation, wait for a ready replacement target, then follow
  `cleanup.md` and `implementation.md` for only the recorded cleanup,
  promotion, and build actions.
- **Cleanup:** Only for an explicit request, follow `cleanup.md`, disable and
  remove exact operation resources, optionally retain or delete the verified
  owned AlphaInsider target, and preserve the retired record.
- **Implemented:** Return changes to `draft`, preserve unaffected decisions,
  interview affected choices, and fully reconfirm.
- **Retired:** Preserve the plan as a non-operational audit record. Resume only
  an explicitly requested pending cleanup; never run the strategy.

Never manually run a one-cycle command, start a persistent process, or trigger
a scheduled task during build or verification. These actions can submit
planned AlphaInsider paper orders without an interactive confirmation. Final
confirmation may authorize an active resource to run at its recorded future
occurrence or login, never as an immediate test run.
