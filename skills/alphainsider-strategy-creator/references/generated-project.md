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
- AlphaInsider target source, name, paper starting scale, public or private
  state, conditional paid setting, public strategy ID, and working link;
- native AI scheduler provider, task name, cadence, timezone, daylight-saving
  behavior, next run, pause state, and history location;
- how the user asks an AI chat for a normal run or dry run;
- the fact that scheduler **Run now** and chat normal runs can submit
  AlphaInsider paper orders without another prompt;
- self-heal settings and notification event policy and channels;
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
- require the installed Strategy Creator skill for creation, updates, deletion,
  target changes, and automation reconfiguration;
- let normal runs and agreed self-healing follow the project and runbook without
  requiring the installed skill;
- list exact project test, backtest, and finite-cycle commands;
- list the native task identity and relevant environment-variable names;
- explain the shared lock and durable trading block;
- forbid exposing secrets or opening complete `.env` files;
- forbid orders during build, tests, backtests, and dry runs;
- protect plan semantics, `pending-update.md`, target identity and settings, cadence,
  credentials, canonical trading history, lock code, repair evidence, and
  protected tests from self-heal changes; and
- tell scheduled agents to read `runtime/runbook.md`.

Keep project-specific facts only. Do not copy interview or credential
procedures.

## Runtime runbook

`runtime/runbook.md` must be sufficient for a new scheduled AI instance with no
chat history or installed Strategy Creator skill. Include:

- exact project identity and current task purpose;
- normal and dry-run entry behavior;
- code-led, agent-led, or hybrid decision steps;
- agreed input sources and decision boundaries;
- exact test and finite-cycle commands;
- lock, scheduled-for-time, missed-run, and overlap rules;
- applicable AlphaInsider compatibility preflight checks and safe no-action
  behavior;
- target validation, reconciliation, risk, and duplicate checks;
- structured result fields;
- evaluation, mandatory run-error pause, the notification-only exception,
  durable block, self-heal, rollback, and verified user-directed recovery rules;
- notification labels, event policy, channels, safe destination configuration
  names, and quiet-success policy; and
- paths for state, history, journal, snapshots, and reports.

Do not put a secret or mutable copy of the strategy agreement in the runbook.
Point to `plan.md` for all high-level behavior.

## Outcome handoffs

Use one heading that matches the completed work:

- **Plan saved** when the user ends before a valid backtest. State plainly
  whether the strategy rules were agreed or remain a draft. Show the strategy
  name, strict asset type, project and plan locations, important open
  limitations, and how to ask an AI to resume later.
- **Backtest complete** after the user ends with a valid backtest. Show the
  strategy name, strict asset type, concise result and limitations, report and
  project locations, and how to ask an AI to resume later.
- **Setup stopped** when the user stops after implementation agreement but
  before automated completion. Show all created local and external resources,
  AlphaInsider target and link when present, scheduled task name and pause
  state, whether paper orders are blocked, project location, last completed
  action, and where setup will resume. Explain how to request resume or
  explicit deletion.

For these non-automated handoffs, do not show the broker resource or ask
another question. The resume instruction is sufficient.

After successful automation, give the **Strategy created successfully**
message. Show:

- strategy name and strict asset type;
- public or private state and paper starting scale;
- paid state and launch price when applicable;
- working AlphaInsider strategy link;
- schedule, timezone, next occurrence, and task name;
- self-heal and notification state;
- project location; and
- backtest report link when one exists.

Then present connecting the AlphaInsider strategy to a broker as an optional
recommended next step. Embed the current broker-automation video when the
interface supports it. Otherwise, link:

[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades)

State that live broker mode can use real funds. Do not recommend paper or live
broker mode. Do not request broker credentials or create the connection. End
the guided creation journey after this handoff without another next-step
question.
