# Persistent Project

Read this file at the start. Select the safest persistent location available.
Do not ask the user where to put the project. If the user names a location,
use it only when it passes the same checks.

## Persistence requirements

The location must outlive this chat and remain available to a new chat. Before
automation, prove that scheduled AI runs can read and write the same project.
The project must preserve `plan.md`, source, tests, backtest output, runtime
state, locks, run history, and repair records.

Do not use chat memory, a temporary upload area, a cache, an installed skill
directory, or another session-only filesystem as project storage.

For a hosted or web platform, prefer its persistent project or workspace when
new chats and scheduled runs can access it. Otherwise, use an already connected
durable repository or storage integration. Do not provision an unrelated cloud
service. If no persistent writable location exists, give one clear action to
enable or connect one and stop before creating files.

For a local platform, prefer the current durable workspace or a suitable
user-controlled projects directory. Create a dedicated child directory. Do not
mix a strategy into an unrelated software project or write into this skill.

Planning storage and scheduled-run access are separate checks. A project can
support the interview and backtest while automation remains blocked. Record
that blocker and the exact next step in `plan.md`.

## Find or create the project

Recognize a project by a root `plan.md` that follows the
[plan template](plan-template.md): exactly one `# Strategy Plan` title and one
`## Current status` section with the documented Phase, Plan agreement, Highest
completed outcome, and Automation state fields. Do not require YAML
frontmatter. Before any run, require each status value to match the template;
stop and reconcile an invalid value.

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
.env
.env.example
.gitignore
README.md
AGENTS.md
strategy/
backtest/
runtime/
tests/
```

Create `.env` only through `scripts/set_env_value.py` when project-file secret
storage is selected. A hosted secure secret store can replace `.env` when the
scheduled runtime cannot use project secrets safely. Add only the dependency
and tool files the implementation needs.

Put the scheduled-agent instructions in `runtime/runbook.md`. Keep mutable
state, locks, histories, and repair records under `runtime/`. Persist
project-relative paths except where the native scheduler requires a stable
external project identity.

Announce the resolved project once. Update `plan.md` after every answer,
material finding, completed step, failure, or next-step change.
