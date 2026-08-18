# Strategy Implementation

Read this reference only after a complete plan is confirmed, when executing a
confirmed replacement or cleanup, or when maintaining an implemented strategy.

## Contents

- [Execution gates](#execution-gates)
- [Replacement execution](#replacement-execution)
- [Cleanup execution](#cleanup-execution)
- [Project build](#project-build)
- [Generated documentation](#generated-documentation)
- [Completion and maintenance](#completion-and-maintenance)

## Execution gates

Read the sibling `alphainsider` skill and only the API references needed for
authentication, instruments, orders, sizing, and selected WebSockets. Before
writing, inventory every path again. Confirmation authorizes new files and
every exact overwrite recorded in the plan. If an unplanned path or collision
appears, return the plan to `draft` and reconfirm the complete updated plan
instead of requesting a one-off approval.

Keep project writes inside the selected project root; use absolute paths only
during the run and persist project-relative paths. Exact confirmed user-level
native operation definitions are the sole host-write exception and confirmed
agent schedulers are external managed resources. Create either only under
`operation-and-scheduling.md` after all preceding gates pass.

For a `ready` target, complete **Confirmed provisioning** in
`alphainsider-target.md` before implementation files. A replacement first
quiesces the attributable outgoing runner under `cleanup.md`, provisions and
validates the ready replacement target, and only then applies the outgoing
remote disposition. For a `local-only` target, make no remote calls, complete
the local build with mocked external interactions for a new or updated
strategy, create no native definition or agent task, and leave the plan
`confirmed`. A local-only replacement leaves the outgoing strategy, binding,
implementation, and operation resources unchanged.

## Replacement execution

For a confirmed replacement, follow `cleanup.md`. Perform only the recorded
actions. A local-only replacement stops before any outgoing cleanup or
promotion. For a ready replacement, disable the outgoing runner and wait for a
safe cycle boundary, then resolve, provision when applicable, validate, and
persist the replacement target.

After replacement readiness, remove and verify the outgoing native definitions
or agent tasks, then apply its target disposition. Remove only exact
attributable source, tests, copied AlphaInsider helpers, dependencies,
`.env.example`, generated `README.md`, and generated `AGENTS.md` listed in the
confirmed plan. Preserve `.env`, `.gitignore`, credentials, caches, historical
data, unrelated files, and every resource whose ownership is uncertain. Never
recursively delete the project root.

Delete the outgoing `docs/plan.md`, then replace `docs/plan.md` with
`docs/replacement-plan.md`, remove the temporary path, and build from the
promoted plan. If outgoing remote deletion alone fails, keep the outgoing ID
on the new plan and allow the ready replacement's confirmed future activation
with a prominent warning. Any shutdown, operation-removal, promotion, or
local-cleanup failure blocks activation. Leave the new plan `confirmed` unless
every required replacement gate succeeds.

## Cleanup execution

Execute an explicit retirement only from a confirmed `docs/plan.md`.
Revalidate every exact path, operation resource, runtime identity, target ID,
and ownership under `cleanup.md`. Disable future cycles, wait for safe
completion, remove exact operation resources, apply the confirmed remote
retain-or-delete disposition, and then remove only the attributable generated
artifacts in the plan.

Preserve the project root, `.env`, `.gitignore`, credentials, caches,
historical logs and state, backtest outputs, unrelated files, and uncertain
resources. Mark `docs/plan.md` as `retired` and keep the strategy ID on that
retired record. If remote deletion fails after safe operation shutdown,
complete local retirement, retain the pending outgoing ID for explicit
resumption, and never retry it during unrelated work.

## Project build

Build the smallest standalone project that satisfies the plan:

- Default to Python. Use another language only for a recorded ecosystem reason
  with equivalent AlphaInsider integration. Create `strategy/`, `tests/`,
  `.env.example`, dependency configuration, `.gitignore`, `README.md`, and
  `AGENTS.md` without a generic framework.
- For Python, read the sibling `scripts/alphainsider_request.py` as an immutable
  source and copy it to `strategy/alphainsider_request.py`. Copy
  `scripts/alphainsider_stream.py` only when the plan uses WebSockets. Pass
  `reconnect=True` to `stream_events` only for confirmed continuous recovery;
  retain one-session behavior when the plan stops on a stream error. Import
  generic request and calculation helpers, add only needed project-local
  endpoint functions, and modify only project copies.
- Put only names and safe examples in `.env.example`. Ignore `.env`, secrets,
  caches, and build outputs; keep plans, source, tests, and docs commit-ready.
  Follow `credentials.md` for missing values.
- Expose project-native commands for one finite decision cycle, a persistent
  process when planned, tests, and a selected backtest. A recurring schedule
  must invoke the same finite one-cycle entry point once per occurrence. Do not
  add dry-run mode or an interactive confirmation before planned paper orders.
  A user-run command is the user's execution action; never manually run a
  cycle, start a persistent process, or trigger a schedule during build and
  verification. For a local-only target, document operational commands but mark
  them unavailable until target readiness is resolved.
- For every finite-cycle and persistent entry point, acquire a fail-closed
  process-lifetime lock before external data or order work and release it
  automatically when the process exits. Include only non-secret project,
  invocation, process or run identity, and start-time attribution. Use an
  equivalent shared lock when multiple remote instances can run the strategy.
  Add offline tests proving a second overlapping occurrence exits before
  signal, reconciliation, or order behavior and a stale marker is not removed
  while its attributable process or occurrence remains active.
- Make a persistent entry point handle the platform's normal graceful-stop
  request by preventing another internal cycle, allowing the active cycle to
  reach its planned safe boundary, releasing its runtime marker, and exiting.
  Test that behavior offline without starting the strategy command.
- Implement the planned fixed, dynamic, or constrained-dynamic selection. For
  runtime candidates without exact IDs, use `search_stocks`; reject missing or
  ambiguous results and never guess a mapping. Validate resolved IDs with `get_stocks`,
  batch when practical, require the planned `security` type, and apply the
  freshness rule. Never order an invalid candidate; continue with valid
  candidates or abort as planned.
- Reconcile relevant AlphaInsider positions and open orders before decisions,
  validate target type at startup, and implement planned data, retry,
  duplicate, recovery, logging, sizing, and risk behavior. Never default a
  missing `input_multiplier` to `1`.
- Keep decisions testable. Backtests replay production logic chronologically
  without AlphaInsider calls or future information, reconstruct dynamic
  candidate sets without survivorship bias, and add portfolio accounting only
  with credible execution and cost assumptions.
- Add offline tests for signals, risk, order mapping, orchestration, and any
  backtest; mock external services. Verification must never submit an order or
  run an order-submitting command.

## Generated documentation

Write `README.md` for humans with purpose, behavior, prerequisites, setup,
environment names, commands, monitoring, limitations, and recovery. Apply the
target reference's API-key and cleanup requirements. Include a short `## Start`
section with ordered, copy-paste commands for dependency installation and
`.env` preparation. Label a single cycle, persistent operation when available,
and recurring scheduling equally. Match the selected language. For Python,
place `source .venv/bin/activate` immediately before the execution commands. For
another language, use the project's exact package-manager and runtime commands
and omit Python steps.

For a local-only target, state that operational commands are unavailable until
the plan is reconfirmed with a ready target. For a ready target, warn that a
user-run command or future active schedule can submit paper orders without
another prompt. Include the selected runner's installation, lifecycle,
schedule, management, logging or history, notification, limitation, and
activation warnings from `operation-and-scheduling.md`.

Write `AGENTS.md` to make `docs/plan.md` authoritative and require the
installed strategy-creator skill before changing, scheduling, or retiring the
strategy. List only this project's commands, runner identity, and env names.
Do not copy interview, cleanup, or credential procedures. Never show
`set_env_value.py` to the user.

## Completion and maintenance

Run all offline tests and static checks. Before setting `implemented`, replace
the plan's `not initiated` cleanup values with the exact project-relative
managed-artifact inventory and `active` retirement state, the current operation
resource identity or unmanaged foreground state with cleanup marked not
requested, and the active target lifecycle disposition. Never infer those
values later from names alone.

For a ready target, complete
**Description synchronization**, then install and verify every confirmed
native definition or agent scheduler in its confirmed active or inactive
state. Never manually trigger it; report the next occurrence for an active
schedule when known. A created agent-scheduler task object counts as
installed even when recorded limitations remain. Set `implemented` only after
the remote and applicable operation gates pass; a local-only target or failed
required background-process installation remains `confirmed`. Exclude
other deployment unless separately requested. Before handoff, verify every
changed path or external task is exact, attributable, and confirmed, and
neither skill changed.

For behavior changes to an `implemented` plan, return it to `draft`, interview
only affected decisions, and reconfirm before code edits. Update code, tests,
`README.md`, and `AGENTS.md` together; regenerate the remote description and
restore `implemented` only after every gate passes. For a runtime-affecting
change, follow `operation-and-scheduling.md`: pause or disable future cycles,
allow an active cycle to finish, stop a persistent process at a safe boundary,
and never resume automatically. Report the final state and exact user-run
resume command.

To resume a confirmed local-only target, return the plan to `draft`, preserve
the offline implementation and unaffected decisions, resolve only target gaps,
and reconfirm before provisioning, synchronization, or other remote work.

For a `retired` plan or a pending outgoing deletion, never run strategy code or
resume a runner. Follow `cleanup.md` only when the user explicitly requests
cleanup or recovery, and otherwise preserve the audit record unchanged.
