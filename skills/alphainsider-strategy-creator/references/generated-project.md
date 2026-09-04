# Generated Project Guidance

This file owns generated `README.md`, `AGENTS.md`, scheduled-run instructions
in `runtime/runbook.md`, and outcome handoffs. Keep them project-specific. Do
not copy the skill's interview or generic procedures.

## Human README

Write a concise README that covers:

- strategy purpose, stock or cryptocurrency type, assets, decisions, data,
  confirmed native-scheduler timing, execution-specific exposure, mapped
  AlphaInsider operation and material side effects, known limits, and that
  `plan.md` is authoritative;
- fixed-code, AI-decision, or code-and-AI responsibilities;
- every backtest's command, future-information use, differences, limitations,
  disposition, source snapshot or durable commit, saved result visuals, and
  report, featuring the latest Valid result that matches the current strategy
  rather than the best result, and retaining recoverable source until explicit
  deletion;
- safe configuration names and location, never values;
- whether the AlphaInsider strategy was created or reused, its name, simulated
  starting value, access setting, AlphaInsider strategy ID, and working link;
- scheduled task, frequency, timezone, daylight-saving behavior, next run,
  Automation state, Operational health, next retry when degraded, and history
  path;
- scheduler **Run now**, chat run, and chat dry run controls, including that
  order-capable runs can submit plan-compliant paper orders without another
  prompt;
- self-heal settings, notification events and channels, and whether each
  notification method is supported or user-selected and unverified, including
  whether notification repair is inside the enabled self-healing scope;
- recovery, update, and explicit deletion requests; and
- after creation is complete, the stable broker-automation resource link.

Do not present direct terminal execution as the user's normal control. For a
project `.env`, recommend active-chat entry first and direct editing second.
Never expose the credential helper command.

State that performance is not guaranteed. Poor performance does not stop a
strategy that follows the plan. Never claim that a notification was delivered
or tested during setup. When future-information use is **Yes**, put the
mandatory warning before backtest results and beside every affected
measurement. Omit the broker resource while creation is incomplete; add it
only after all completion gates pass.

## Project agent guide

Generated `AGENTS.md` must:

- make `plan.md` authoritative and route scheduled agents to
  `runtime/runbook.md`;
- require Strategy Creator for creation, updates, deletion, AlphaInsider
  strategy changes, and scheduler reconfiguration, but not strategy runs or
  confirmed self-healing;
- list exact project test, backtest, and strategy-run commands; the
  scheduled task name; and safe configuration names;
- explain the creation, strategy, backtest, AlphaInsider setup, and
  automation status fields, including Operational health; the shared lock; how
  user/update/deletion/setup state pauses new orders; and why an operational
  error keeps automation Active while gating unsafe orders; and
- forbid secret exposure, opening or inspecting the complete `.env`, and
  orders during builds, tests, backtests, or dry runs. Protect plan
  semantics, `pending-update.md`, AlphaInsider strategy identity and settings,
  scheduler identity and frequency, credentials, saved trading history, lock
  code, repair evidence, and protected tests from self-healing.

## Scheduled-run instructions

The `runtime/runbook.md` file must let a new scheduled AI instance operate
without chat history or this installed skill. Include the project-specific
requirements from `implementation.md` and `scheduled-runs.md`, including:

- project identity; strategy run and dry run entry; decision responsibilities;
  exact commands; and hard risk limits;
- the lock, scheduled time, missed-run, overlap, compatibility, AlphaInsider
  strategy, documented-or-fallback session policy, expected closed-market
  skips, position, open-order, saved-state, duplicate, and structured-result
  rules, including one completed run per trigger and no faster-cadence polling
  or background loop;
- the rule that an operational error ends order work for that trigger, keeps
  Automation state Active, sets Operational health to Degraded/Retrying, and
  retries checks on the next trigger; the order gate for unresolved and
  ambiguous results; no same-trigger order retry or missed-order replay; repair
  limits; protected resources; snapshots; rollback; and verified recovery; and
- notification labels, selected events, independent channels, safe destination
  names, first-and-material-change deduplication, best-effort delivery failure
  behavior, and state, history, journal, snapshot, and report paths.

Do not put a secret or a separate editable copy of strategy behavior in
`runtime/runbook.md`. Point to `plan.md` for the confirmed strategy.

## Outcome handoffs

During creation, lead every user stop or technical blocker with **Creation
incomplete**. State the reason, creation phase, strategy status, highest
completed outcome, project and plan locations, last completed action, exact
resume step, and how to resume. Do not use this handoff for an operational
error after creation already completed; completion remains intact while its
run status becomes Degraded/Retrying.

Add the applicable evidence:

- for a Draft or confirmed strategy, summarize the strategy and open decisions;
- after backtesting, show each `Backtest <date or ID> — Valid | Superseded |
  Failed`, its future-information use, differences, limitations, concise
  findings, report location, and which Valid result matches the current
  strategy. When future-information use is **Yes**, put the mandatory warning
  before the findings and beside affected measurements; and
- during AlphaInsider setup, inventory local and external resources, the
  AlphaInsider strategy and link, scheduled task state, and whether scheduled
  runs and new orders are paused.

Whenever an incomplete or terminal handoff presents backtest findings, reuse
the exact saved result visuals for the featured Valid run that matches the
current strategy. Usually show its two to four planned visuals. Embed them when
supported; otherwise link directly to each named image. The detailed report
link is additional and never replaces the result visuals. Include an earlier,
Superseded, or Failed run's diagnostic visual only when it materially helps.
Keep every warning required by [backtesting](backtesting.md) inside and beside
the affected visual. If a planned visual remains unavailable after its safe
repair attempt, state only that some planned visuals are unavailable and show
the available findings normally. A later repair must use the same saved run
outputs and preserve the original failure record.

Do not show the broker resource or ask another guided-creation question in an
incomplete handoff. A resume instruction is sufficient.

Only after every completion gate passes, choose the accurate terminal title:

- **Strategy created successfully** when this project created a new
  AlphaInsider strategy; or
- **Strategy automation completed successfully** when it reused an existing
  AlphaInsider strategy.

Include the strategy and asset type, AlphaInsider settings and link, schedule
and scheduled task, self-heal state, notification choices and support status,
project location, and backtest findings, saved result visuals, and reports when
present. This terminal handoff is informational and asks for no approval.

Then use the optional-next-step format in
[user communication](user-communication.md) with the short title **Connect a
broker**. Embed the current video when supported; otherwise link
[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades).
State that live broker mode can use real funds. Do not choose paper or live
broker mode, request broker credentials, create the connection, or ask another
guided-creation question.
