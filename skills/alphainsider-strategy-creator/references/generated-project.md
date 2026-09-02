# Generated Project Guidance

Read this file when creating or updating `README.md`, `AGENTS.md`,
`runtime/runbook.md`, or the final handoff. Keep project-specific facts in the
project. Do not copy this skill's full procedures.

## Human README

Write a concise README with:

- purpose, strict asset type, instrument universe, and strategy summary;
- the fact that `plan.md` is authoritative;
- code-led, agent-led, or hybrid responsibilities;
- data sources, timing, risk, maximum leverage, and known limits;
- backtest command, report locations, results summary, and limitations;
- environment variable names and secret location, never values;
- AlphaInsider public strategy ID and working strategy link;
- native AI scheduler provider, task name, cadence, timezone, daylight-saving
  behavior, next run, pause state, and history location;
- how the user asks an AI chat for a normal run or dry run;
- the fact that scheduler **Run now** and chat normal runs can submit
  AlphaInsider paper orders without another prompt;
- self-heal and notification settings;
- recovery, update, and explicit deletion requests; and
- the stable broker-automation resource link.

Do not tell the user to run the strategy program directly in a terminal as the
normal manual control. Internal commands can remain documented for agents and
development. For project `.env`, recommend active-chat entry first and direct
editing second. Never expose the credential helper command.

State plainly that strategy performance is not guaranteed. Poor performance
does not stop a plan-conforming strategy.

## Project agent guide

Generated `AGENTS.md` must:

- make `plan.md` authoritative;
- require the installed Strategy Creator skill before changing, scheduling,
  repairing, running, or deleting the strategy;
- list exact project test, backtest, and finite-cycle commands;
- list the native task identity and relevant environment-variable names;
- explain the shared lock and durable trading block;
- forbid exposing secrets or opening complete `.env` files;
- forbid orders during build, tests, backtests, and dry runs;
- protect plan semantics, `pending-update.md`, target identity, cadence,
  credentials, canonical trading history, lock code, repair evidence, and
  protected tests from self-heal changes; and
- tell scheduled agents to read `runtime/runbook.md`.

Keep project-specific facts only. Do not copy interview or credential
procedures.

## Runtime runbook

`runtime/runbook.md` must be sufficient for a new scheduled AI instance with no
chat history. Include:

- exact project identity and current task purpose;
- normal and dry-run entry behavior;
- code-led, agent-led, or hybrid decision steps;
- approved input sources and decision boundaries;
- exact test and finite-cycle commands;
- lock, scheduled-for-time, missed-run, and overlap rules;
- applicable AlphaInsider compatibility preflight checks and safe no-action
  behavior;
- target validation, reconciliation, risk, and duplicate checks;
- structured result fields;
- evaluation, error pause, durable block, self-heal, rollback, and resume
  rules;
- notification labels, channel, destination, and quiet-success policy; and
- paths for state, history, journal, snapshots, and reports.

Do not put a secret or mutable copy of the strategy agreement in the runbook.
Point to `plan.md` for all high-level behavior.

## Final success handoff

After completion, give a clear **Strategy created successfully** message. Show:

- strategy name and strict asset type;
- working AlphaInsider strategy link;
- schedule, timezone, next occurrence, and task name;
- self-heal and notification state;
- project location; and
- backtest report link when one exists.

Then explain that the user can connect the AlphaInsider strategy to a broker.
Embed the current broker-automation video when the interface supports it.
Otherwise, link:

[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades)

State that live broker mode can use real funds. Do not recommend paper or live
broker mode. Do not request broker credentials or create the connection. End
the guided creation journey after this handoff without another next-step
question.
