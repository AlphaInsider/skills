# Generated Project Guidance

This file owns generated `README.md`, `AGENTS.md`, `runtime/runbook.md`, and
outcome handoffs. Keep them project-specific. Do not copy the skill's interview
or generic procedures.

## Human README

Write a concise README that covers:

- the strategy purpose, strict asset type, universe, rules, data, timing, risk,
  leverage, known limits, and that `plan.md` is authoritative;
- code-led, agent-led, or hybrid responsibilities;
- the backtest command, report paths, result summary, and limitations;
- safe configuration names and location, never values;
- target source, name, starting scale, access and paid settings, public ID, and
  working link;
- native task identity, cadence, timezone, daylight-saving behavior, next run,
  state, and history path;
- chat normal-run and dry-run controls, including that scheduler **Run now**
  and chat normal runs can submit paper orders without another prompt;
- self-heal and notification settings, recovery, update, and explicit deletion
  requests; and
- the stable broker-automation resource link.

Do not present direct terminal execution as the user's normal control. For a
project `.env`, recommend active-chat entry first and direct editing second.
Never expose the credential helper command.

State that performance is not guaranteed. Poor performance does not stop a
plan-conforming strategy.

## Project agent guide

Generated `AGENTS.md` must:

- make `plan.md` authoritative and route scheduled agents to
  `runtime/runbook.md`;
- require Strategy Creator for creation, updates, deletion, target changes, and
  scheduler reconfiguration, but not for normal runs or agreed self-healing;
- list exact project test, backtest, finite-cycle commands, native task
  identity, and configuration names;
- explain the shared lock and durable trading block; and
- forbid secret exposure, opening or inspecting the complete `.env`, and orders
  during builds, tests, backtests, or dry runs. Protect plan semantics,
  `pending-update.md`, target identity and settings, scheduler identity and
  cadence, credentials, canonical trading history, lock code, repair evidence,
  and protected tests from self-healing.

## Runtime runbook

The runbook must let a new scheduled AI instance operate without chat history
or this installed skill. Materialize the project-specific contracts from
`implementation.md` and `scheduled-runs.md`, including:

- project identity; normal and dry-run entry behavior; decision mode; allowed
  inputs and judgments; exact commands; and hard risk limits;
- the lock, scheduled time, missed-run, overlap, compatibility, target,
  reconciliation, duplicate, and structured-result rules;
- mandatory error pause, the notification-only exception, durable block,
  repair limit, protected resources, snapshots, rollback, and verified
  recovery; and
- notification labels, event policy, channels, safe destination names, and all
  state, history, journal, snapshot, and report paths.

Do not put a secret or a mutable copy of strategy behavior in the runbook.
Point to `plan.md` for the agreement.

## Outcome handoffs

Use the heading selected by `interview.md`:

- **Plan saved:** State whether the rules are agreed or Draft. Show the
  strategy, asset type, project and plan locations, important open limits, and
  how to resume.
- **Backtest complete:** Show the strategy, asset type, concise results and
  limits, report and project locations, and how to resume.
- **Setup stopped:** Inventory local and external resources, target and link,
  task and pause state, trading block, project location, last action, and
  resume point. Explain how to request resume or explicit deletion.

Do not show the broker resource or ask another question in these partial
handoffs. A resume instruction is sufficient.

After successful automation, give a **Strategy created successfully** message
with the strategy and asset type, target settings and link, schedule and task,
self-heal and notification state, project location, and backtest report when
present.

Then offer broker connection as an optional recommended next step. Embed the
current video when supported; otherwise link
[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades).
State that live broker mode can use real funds. Do not choose paper or live
broker mode, request broker credentials, create the connection, or ask another
guided-creation question.
