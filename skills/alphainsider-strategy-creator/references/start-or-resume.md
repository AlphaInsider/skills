# Start or Resume

Use this workflow first for every request. It owns persistent-location
selection, project discovery, project creation, and initial routing. Read
[workflow contracts](workflow-contracts.md) before the first user-facing
message.

Project selection and resumption are automatic preflight, not another
user-facing creation stage.

## 1. Select a persistent parent

1. Inspect the current platform and choose the safest writable location that
   will outlive this chat and remain available to a new chat.
2. Prefer a hosted platform's persistent project or workspace when new chats
   and scheduled runs can read and write it.
3. Otherwise, use an already connected durable repository or storage
   integration. Do not create an unrelated cloud service.
4. On a local platform, prefer the current durable workspace or a suitable
   user-controlled projects directory, then use a dedicated child directory.
5. If no persistent writable location exists, give one clear action to enable
   or connect one and stop before creating files.

- Do not ask the user where to put the project. If the user names a location,
  use it only after the same checks pass.
- Do not use chat memory, a temporary upload area, cache, installed skill
  directory, or session-only filesystem.
- Do not mix a strategy into an unrelated software project.
- The location must preserve the plan, source, tests, backtest output, saved
  state, locks, histories, and repair evidence.

Planning storage and scheduled-run access are separate checks. A project can
support definition and backtesting while automation remains blocked. Record
that blocker and its exact next step in `plan.md`.

## 2. Find a matching project

1. Inspect the current directory and nearest suitable ancestors.
2. Inspect immediate children of the selected persistent parent.
3. Consider a new dedicated child only when no clear existing match applies.

Recognize a project by a root `plan.md` with exactly one `# Strategy Plan`
title and one `## Current status` section. A current plan contains the fields
and status enums in the [plan template](plan-template.md). Accept both the new
ranked layout and the former flat section layout; layout alone never makes a
project legacy.

Treat a plan as an older version of the same project—not an unrelated
directory—when it has any of these schema indicators:

- the former **Plan agreement** field or former Plan outcome value;
- the former **Maximum strategy leverage** field;
- an Error automation-pause reason;
- missing current Define-time scheduler, execution, session-policy, or
  AlphaInsider-constraint fields; or
- missing current lifecycle status fields.

Use the migration in [project contract](project-contract.md) before any run.

- Do not require YAML frontmatter.
- Do not crawl unrelated source or open `.env`.
- Resume a single project that clearly matches the user's words.
- If several projects match, ask which one and include **Create a new
  strategy**.
- A request for another strategy creates a sibling, never a nested project.

## 3. Resolve the project

Choose one branch from the discovery result.

### Create a project when needed

1. Ask the strategy objective first.
2. Derive a short lowercase kebab-case directory name from that objective.
3. Use the next free numeric suffix when the name already exists.
4. Confirm that the chosen child is new or safe to adopt.
5. Create the core layout in [project contract](project-contract.md) and copy
   the [plan template](plan-template.md) into root `plan.md`.
6. Record the stated objective, resolved location, last completed step, next
   step, waiting state, and current UTC update time.

Never overwrite or adopt an unrelated directory. Do not create `.env` during
initialization; the protected credential workflow creates it only if project
file secret storage is later selected.

### Resume an existing project

1. Read `plan.md` and **Current status** from disk. Never reconstruct it from
   chat memory.
2. Migrate an older schema through [project contract](project-contract.md)
   before a run or mutation.
3. Continue from **Next step** unless the user's current words clearly request
   another supported action.
4. Recheck only facts needed by the resumed phase, including applicable
   AlphaInsider limits, identity and settings, native scheduler state,
   persistent access, and secret access.
5. Reconcile any ambiguous or partial external outcome before retrying. Never
   create a replacement merely because the earlier result is unclear.

Infer a clear request for an update, chat run, dry run, inspection, or deletion
without asking another action question. Ask only when several projects or
actions remain plausible.

## 4. Route the work

1. For new creation, incomplete definition, or reopened strategy decisions,
   read [define strategy](define-strategy.md).
2. For selected backtest feasibility, planning, execution, or results, read
   [backtest strategy](backtest-strategy.md).
3. For AlphaInsider access, setup, implementation, or activation, read
   [implement and activate](implement-and-activate.md).
4. For a scheduled run, scheduler **Run now**, chat run, dry run, operational
   error, notification, or self-heal attempt, read
   [run and recover](run-and-recover.md).
5. For a requested strategy change, detected edit, or external drift, read
   [update strategy](update-strategy.md).
6. For explicit deletion, read [delete strategy](delete-strategy.md).

Announce the resolved project once. Thereafter, follow the plan-update and
stop/resume rules in [workflow contracts](workflow-contracts.md).
