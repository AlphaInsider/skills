---
name: alphainsider-strategy-creator
description: Create, resume, backtest, implement, automate, update, or explicitly delete one plan-driven AlphaInsider paper-trading strategy. Use for stock or cryptocurrency strategies that run through a native AI scheduler and may use code, the scheduled AI agent, or both.
---

# AlphaInsider Strategy Creator

Guide one strategy from idea to an active AlphaInsider paper strategy. Keep the
installed skill read-only. Create all user artifacts in one persistent project.

## Boundaries

- `plan.md` is the project's readable source of truth. Code, backtests, the
  AlphaInsider target, and automation must conform to it.
- One project contains one strategy with one strict `stock` or
  `cryptocurrency` type. Dynamic selection must stay inside that type.
- Before offering, building, or performing an AlphaInsider action, check its
  current applicable constraints and allow only supported behavior. Recheck
  constraints that can change immediately before the action.
- Send orders only to AlphaInsider paper strategies. Never create a broker
  client, connect a broker, or request broker credentials.
- Never inspect, print, or summarize an existing API key, secret store, or
  complete `.env`. Values deliberately pasted in chat may be stored only with
  the non-echoing helper in `scripts/set_env_value.py`.
- Use only the platform's native AI automation or scheduler. Never install
  cron, a system service, an operating-system task scheduler, or a background
  process.
- Make the generated `plan.md` and runbook sufficient for normal runs and
  agreed self-healing without this installed skill. Require this skill for
  creation, updates, deletion, and automation reconfiguration.
- Treat profit and loss as information. Poor performance never makes a
  plan-conforming run unhealthy and never authorizes automatic strategy
  changes.
- Use only create, resume, update, and explicit deletion paths. A materially
  different strategy belongs in another project. Handle deletion only after an
  explicit user request.

## Start or resume

1. Read [`references/user-communication.md`](references/user-communication.md)
   and [`references/project-root.md`](references/project-root.md).
2. Select the safest persistent location without asking the user. Resume the
   matching project when one is clear. Otherwise, create one dedicated project
   after its objective is known.
3. Read [`references/plan-template.md`](references/plan-template.md) and
   [`references/interview.md`](references/interview.md). Maintain `plan.md`
   after each answer or completed action. Keep **Current status** sufficient
   for another chat or scheduled agent to continue without this transcript.
4. For an existing project, infer whether the user wants to resume, update,
   run, dry-run, inspect, or delete it. Ask only when the intent or project is
   ambiguous.

## Creation flow

Follow this order and always lead the user to the next available step:

1. Interview for the high-level strategy and obtain agreement.
2. Offer and recommend a credible backtest. Follow
   [`references/backtesting.md`](references/backtesting.md) when accepted.
3. Build the backtest, show clear charts and metrics, record limits, and settle
   any strategy changes with the user.
4. Offer and recommend AlphaInsider forward testing.
5. When accepted, inspect persistent-project and non-prompt secret access
   without asking a user question. Use that result to select safe credential
   storage, then follow
   [`references/credentials.md`](references/credentials.md). Request a missing
   key as the first user action in one standalone message; privately verify an
   existing configured key without requesting it again.
6. Follow
   [`references/alphainsider-target.md`](references/alphainsider-target.md).
   Discover the account and compatible owned targets, ask the target choice in
   its own round, then settle only the selected target's settings.
7. Complete the current platform's native scheduler capability check. Map the
   agreed decision mode and schedule, then settle self-healing and notifications
   in dependency order.
8. Show the complete implementation agreement described in
   [`references/interview.md`](references/interview.md).
9. Follow [`references/implementation.md`](references/implementation.md).
   Build and pass offline, order-free checks before creating a new target.
10. Create or bind the target, apply only agreed target changes, and follow
   [`references/automation.md`](references/automation.md) to activate one
   native AI schedule for the next normal occurrence.
11. Mark the requested outcome complete and follow the matching outcome
    handoff in
    [`references/generated-project.md`](references/generated-project.md).

If the user declines an optional stage, record that choice and continue to the
next useful stage. If a prerequisite cannot be met, preserve completed work,
record the exact blocker and next step, and do not claim completion beyond the
highest completed outcome.

If the user stops creation, follow the centralized mapping in `interview.md`.
A stop never authorizes deletion. Preserve partial resources and make any
active schedule safe.

## Agreement and authority

Use these independent status fields; do not collapse them into one lifecycle:

- **Phase:** Interviewing, Building backtest, Reviewing results, Building
  implementation, Configuring automation, or Complete.
- **Plan agreement:** Draft or Agreed.
- **Highest completed outcome:** None, Plan, Backtest, or Automated strategy.
- **Automation state:** Not configured, Active, or Paused.

These are stored project values, not user-facing journey labels. Describe the
actual work in plain language. Keep each user choice limited to its current
decision, and introduce later optional work only after that decision is
settled. Follow `references/user-communication.md` for transition wording.

Change **Plan agreement** to Draft while an open decision can change intended
strategy behavior. Ask the user to agree to the normalized plan before building
that stage. Keep **Phase** at Interviewing while creation decisions remain open;
set it to Building implementation only after the implementation plan is agreed.
During an update, keep the current plan Agreed and mark `pending-update.md`
Draft until the change is agreed. Agreement authorizes only its recorded
actions. The agreed automation plan also authorizes future plan-conforming
paper orders without per-order confirmation.

If implementation or backtesting reveals that an agreed high-level decision
must change, stop the affected work and return to the interview. Routine fixes
such as compatible endpoint wiring, rate-limit handling, or other
plan-preserving mechanics need no new strategy decision.

## Conditional references

Do not preload every reference. Read each relevant file in full when its phase
or action begins:

- [`references/scheduled-runs.md`](references/scheduled-runs.md) — every
  scheduled run, scheduler Run now, chat normal run, chat dry run, error,
  notification event, or self-heal attempt.
- [`references/generated-project.md`](references/generated-project.md) —
  project files, human README, agent guide, runbook, and final handoff.
- [`references/changes-and-deletion.md`](references/changes-and-deletion.md) —
  updates, user edits, drift, or explicit deletion.

When `alphainsider-api` is installed, read its `SKILL.md` and only the API
sections needed for the current action. Otherwise, use the current
`https://api.alphainsider.com` index and contracts. For credential collection,
follow `references/credentials.md`; use `alphainsider-api` for API behavior and
retain its no-inspection and no-echo safeguards. Do not duplicate an API catalog
in this skill.
