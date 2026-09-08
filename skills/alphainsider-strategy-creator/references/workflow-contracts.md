# Workflow Contracts

## Interview and communication

Work in rounds of decisions whose prerequisites are settled. Ask the current
round together, then let the answers determine the next round. Research facts
from available tools and documentation; ask the user about intent and choices.
Skip settled questions and choose routine technical details yourself.

Use this format, with useful options and a recommendation for each question:

```markdown
❓ **Q1** - **Short title:** A question in plain language.

A. First option
B. Second option

➡️ **Recommended:** A — a short reason.

---

❓ **Q2** - **Short title:** The next independent question.

A. First option
B. Second option

➡️ **Recommended:** B — a short reason.
```

`Recommended all` accepts the recommendations in the current round. Summarize
settled decisions at meaningful transitions and explain the next step. Honor
existing answers and authorization; ask again only when a material decision
changes or remains unclear.

A required user action gets its own response. Do not ask interview questions
in that response, including through question tools, even when the questions
are independent of the action. Give the action, any alternative, and how to
signal completion, then end the turn. Record the waiting point in `plan.md`;
resume questions after the action is complete and any necessary verification
succeeds.

Use these markers for actions and next steps:

- `👉 **Action — Short title:**` what the user must do and how to signal completion.
- `↪️ **Alternative:**` another supported way to complete that action.
- `➡️ **Next:**` what happens next.

Keep questions, results, and notifications understandable without API names or
implementation details unless those details help the user decide.

## Schedule activation

Enable new schedules automatically for the next scheduled run as part of the
agreed setup, without a separate activation confirmation. If creation returns
a paused task, enable it during the same setup. Clear only setup-created
execution blocks, verify the task is active, and record its identity and next
run in `plan.md`.

Check project and `.env` access, command execution, and pause/resume support
using platform configuration and documented capabilities. A prior scheduled run
is not required proof of access. Leave inactive only for an explicit user pause
or a concrete setup failure; preserve user/error pauses and explain the blocker.
Do not substitute scheduling infrastructure without the user's choice.

## Persistent project and plan

Use a dedicated persistent project available to later chats and scheduled runs.
Honor a selected location and resume a clear existing match; ask when the
project is ambiguous. Never put projects, user plans, or secrets in the skill
repository or temporary chat storage.

Root `plan.md` is the source of truth for high-level strategy, backtest,
implementation, self-healing, notification, and planning decisions. Use the
[plan template](plan-template.md) as a starting outline, adapting its detail to
the project. It is not a fixed field schema or a conversation transcript.

Update the plan as answers, findings, actions, or failures change the work.
Keep the current step, open decisions, last outcome, next action, resource
identities, and actual scheduler state clear. Save an intended external action
before attempting it and record its result afterward so an interrupted chat
can reconcile it. Link code, detailed procedures, reports, and run history;
keep the decisions and a useful summary in the plan itself. Store secrets only
in project `.env`, excluded from version control and generated reports.

Generate a project runbook with commands, expected outcomes, scheduler controls,
and the recovery/notification procedure. Link it from `plan.md` and the scheduled
task. It must let a fresh scheduled agent operate without chat history or this
installed skill; refer to the plan for decisions instead of duplicating them.

The user can stop, resume, or update at any point. Record the exact handoff and
whether automation is still running; clarify an ambiguous request to stop
when existing automation would be affected. For changes to running behavior,
pause automation and coordinate with the run lock before changing files in use.
Preserve settled decisions and artifacts, revisit only affected questions, and
identify backtest results that no longer describe the current strategy. Resume
only when the user's intent and the verified project state permit it.
