# Persistent Project

Read this file at the start. Select the safest persistent location available.
Do not ask the user where to put the project. If the user names a location,
use it only when it passes the same checks.

## Persistence requirements

The location must outlive this chat and remain available to a new chat. Before
automation, prove that scheduled AI runs can read and write the same project.
The project must preserve `plan.md`, source, tests, backtest output, saved run
state, locks, run history, and repair records.

Do not use chat memory, a temporary upload area, a cache, an installed skill
directory, or another session-only filesystem as project storage.

For a hosted or web platform, prefer its persistent project or workspace when
new chats and scheduled runs can access it. Otherwise, use an already connected
durable repository or storage integration. Do not create an unrelated cloud
service. If no persistent writable location exists, give one clear action to
enable or connect one and stop before creating files.

For a local platform, prefer the current durable workspace or a suitable
user-controlled projects directory. Create a dedicated child directory. Do not
mix a strategy into an unrelated software project or write into this skill.

Planning storage and scheduled run access are separate checks. A project can
support the interview and backtest while automation remains blocked. Record
that blocker and the exact next step in `plan.md`.

## Find or create the project

Recognize a project by a root `plan.md` with exactly one `# Strategy Plan` title
and one `## Current status` section. A current plan follows the
[plan template](plan-template.md) and has the documented Creation state, Phase,
Strategy status, Backtest status, AlphaInsider setup status, Highest completed
outcome, Automation state, and Operational health fields. A plan with the
former **Plan agreement** field, former Plan outcome value,
former **Maximum strategy leverage** field, an Error automation-pause reason,
or missing current Define-time scheduler, execution, session-policy, and
AlphaInsider-constraint fields is a legacy version of the same project, not an
unrelated directory. Do not require YAML frontmatter. Before any run, migrate
the legacy schema and require each resulting value to match the current
template.

Search in this order:

1. the current directory and nearest suitable ancestors;
2. immediate children of the selected persistent parent; and
3. a new dedicated child.

Do not crawl unrelated source or open `.env`. If one project clearly matches
the user's words, resume it. If several match, ask which one and include
**Create a new strategy**. A request for another strategy creates a sibling,
not a nested project.

For a new project, ask the objective first. Derive a short lowercase
kebab-case directory name from that objective. Use the next free numeric suffix
for a collision. Never overwrite or adopt an unrelated directory.

## Core project contract

Create and maintain this core layout:

```text
plan.md
.env.example
.gitignore
README.md
AGENTS.md
strategy/
backtest/
runtime/
tests/
```

The `.env` file is conditional, not part of a new project's required initial
layout. Create it only through `scripts/set_env_value.py` after project-file
secret storage is selected. A hosted secure secret store replaces `.env` when
scheduled runs cannot use project secrets safely. Add only the dependency and
tool files the implementation needs.

Put the scheduled-run instructions in `runtime/runbook.md`. Keep project state,
locks, histories, and repair records under `runtime/`. Persist project-relative
paths except where the native scheduler requires a stable external project
identity.

Announce the resolved project once. Update `plan.md` after every answer,
material finding, completed step, failure, or next-step change.

## Migrate a legacy plan schema

Migrate an older Strategy Creator plan in place before resuming it. Preserve
all strategy and setup decisions, historical evidence, resource identities,
and safe resume details. Never open `.env`, repeat an external action, or
create a sibling project only because the status schema is older.

Before changing `plan.md`, save its exact contents to a new timestamped backup
at `runtime/migrations/plan-before-schema-migration-YYYYMMDDTHHMMSSZ.md`, using
the current UTC time and a collision-safe suffix when necessary. Never
overwrite a prior backup. Record the backup path and migration time in the
migrated plan, and retain the backup until explicit deletion.

Use saved artifacts and status together:

- map an agreed strategy, or a Plan, Backtest, or Automated strategy
  outcome, to Strategy status Confirmed; otherwise use Draft;
- map an accepted backtest choice to Backtest choice Selected. Map a
  declined choice to Backtest choice and status Skipped. For a selected backtest,
  set Backtest status to Completed only for a verified Valid artifact that
  matches the current strategy and backtest plan, Authorized only when the old
  phase or last step proves that the backtest plan was authorized, and otherwise
  Draft. Preserve an old unavailable finding but offer Backtest Strategy unless
  the user already chose implementation. Use Highest completed outcome
  Backtest only for that matching Valid evidence; otherwise use Strategy
  defined for a confirmed strategy;
- map an old building or configuring setup phase to AlphaInsider setup status
  Authorized, but map it to Active only after every current completion gate is
  freshly verified;
- map an old Complete phase with no verified active automation to Creation
  state Stopped and reconstruct its nonterminal Phase from the last completed
  step and exact resume point; and
- derive Operational health from durable run history: Not active before
  activation, Ready for verified active automation with no operational run,
  Healthy after the latest plan-compliant run, or Degraded/Retrying after an
  unresolved run error. Preserve the actual native Automation state. If an old
  project was automatically paused for an error, keep it Paused during
  migration rather than silently resuming an external task, preserve the error
  as Degraded/Retrying, and give the user the native resume action.

Translate an old leverage value into maximum strategy exposure without
claiming that it is a universal AlphaInsider limit. Preserve the value, mark
its execution-specific validation unresolved, and map the intended behavior to
the current order operation. For incomplete creation, a previously confirmed
strategy that lacks the current scheduler, session-policy, execution, or
public-limit checks returns to Draft at the affected Define Strategy decision.
A previously completed creation remains Complete when its current completion
gates still verify; unresolved run-time compatibility prevents a new order,
keeps active automation Degraded/Retrying, and uses the next-trigger error flow
rather than rewriting creation history.

Never promote ambiguous legacy work to Authorized, Active, or Complete. Use
the least-authoritative matching status, keep external resources intact, and
resolve a material ambiguity in the next combined summary and next-step prompt.
Record the migration and resulting resume step in `plan.md`.

Creation state can first transition to Complete only when Phase is Complete,
Strategy status is Confirmed, AlphaInsider setup status is Active, Highest
completed outcome is Automated strategy, Automation state is Active,
Operational health is Ready or Healthy, and the completion gates in
`interview.md` are verified. A later operational error does not undo completed
creation or pause automation; keep Creation state and Phase Complete,
Automation state Active, and record Degraded/Retrying with the next retry. A
later user pause also preserves completed creation but sets Automation state to
Paused. During creation, a user stop sets Creation state to Stopped and a
technical gate sets it to Blocked. Both preserve the current nonterminal Phase
and exact resume step.
