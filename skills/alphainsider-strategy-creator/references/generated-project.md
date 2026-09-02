# Generated Project Guidance

This file owns generated `README.md`, `AGENTS.md`, the scheduled-run
instructions in `runtime/runbook.md`, and outcome handoffs. Keep them
project-specific. Do not copy the skill's interview or generic procedures.

## Human README

Write a concise README that covers:

- the strategy purpose, stock or cryptocurrency type, assets it can trade,
  decisions, data, timing, risk, leverage, known limits, and that `plan.md` is
  authoritative;
- fixed code, AI decision, or code and AI responsibilities;
- the backtest command, report paths, result summary, and limitations;
- safe configuration names and location, never values;
- whether the AlphaInsider strategy was created or already existed, its name,
  simulated starting value, public or private access, paid access settings,
  AlphaInsider strategy ID, and working link;
- scheduled task name, schedule frequency, timezone, daylight-saving behavior,
  next run, state, and history path;
- chat run and dry run controls, including that scheduler **Run now** and chat
  runs can submit paper orders without another prompt;
- self-heal and notification settings, recovery, update, and explicit deletion
  requests; and
- the stable broker-automation resource link.

Do not present direct terminal execution as the user's usual control. For a
project `.env`, recommend active-chat entry first and direct editing second.
Never expose the credential helper command.

State that performance is not guaranteed. Poor performance does not stop a
strategy that follows the plan.

## Project agent guide

Generated `AGENTS.md` must:

- make `plan.md` authoritative and route scheduled agents to
  `runtime/runbook.md`;
- require Strategy Creator for creation, updates, deletion, AlphaInsider
  strategy changes, and scheduler reconfiguration, but not for strategy runs or
  agreed self-healing;
- list exact project test, backtest, and strategy run commands; the scheduled
  task name; and configuration names;
- explain the shared lock and how project state pauses new orders; and
- forbid secret exposure, opening or inspecting the complete `.env`, and orders
  during builds, tests, backtests, or dry runs. Protect plan semantics,
  `pending-update.md`, AlphaInsider strategy identity and settings, scheduler
  identity and frequency, credentials, saved trading history, lock code, repair
  evidence, and protected tests from self-healing.

## Scheduled-run instructions

The `runtime/runbook.md` file must let a new scheduled AI instance operate
without chat history or this installed skill. Include the project-specific
requirements from `implementation.md` and `scheduled-runs.md`, including:

- project identity; strategy run and dry run entry behavior; how decisions are
  made; what the AI can use and decide; exact commands; and hard risk limits;
- the lock, scheduled time, missed-run, overlap, compatibility, AlphaInsider
  strategy, position, open-order, saved-state, duplicate, and structured-result
  rules;
- the rule that every real run error pauses scheduled runs and new orders; the
  exception for a failure to send a notification; repair limits; protected
  resources; snapshots; rollback; and verified recovery; and
- notification labels, selected events, channels, safe destination names, and
  all state, history, journal, snapshot, and report paths.

Do not put a secret or a separate editable copy of strategy behavior in
`runtime/runbook.md`. Point to `plan.md` for the agreement.

## Outcome handoffs

Use the heading selected by `interview.md`:

- **Plan saved:** State whether the strategy is agreed or Draft. Show the
  strategy, asset type, project and plan locations, important open limits, and
  how to resume.
- **Backtest complete:** Show the strategy, asset type, concise results and
  limits, report and project locations, and how to resume.
- **Setup stopped:** Inventory local and external resources, AlphaInsider
  strategy and link, scheduled task state, whether scheduled runs and new
  orders are paused, project location, last action, and resume point. Explain
  how to request resume or explicit deletion.

Do not show the broker resource or ask another question in these partial
handoffs. A resume instruction is sufficient.

After successful automation, give a **Strategy created successfully** message
with the strategy and asset type, AlphaInsider settings and link, schedule and
scheduled task, self-heal and notification state, project location, and
backtest report when present.

Then offer broker connection as an optional recommended next step. Embed the
current video when supported; otherwise link
[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades).
State that live broker mode can use real funds. Do not choose paper or live
broker mode, request broker credentials, create the connection, or ask another
guided-creation question.
