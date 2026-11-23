# Workflow Contracts

## Check platform and automation access

1. Before creating files or starting connection work, select persistent storage
   and native AI scheduling for the host runtime, independently of model
   provider or browser/desktop interface.
   - Native includes agent `cron`. Use OS cron/external schedulers only
     if native scheduling is unsupported or the user explicitly requests them.
     Missing tools warrant checking other host interfaces.
   - Web products with Projects must use them; reuse attached/user-confirmed
     Projects. Verify availability for the current account.

   | Runtime | Workspace and scheduler |
   | --- | --- |
   | ChatGPT cloud chat | Project + [Scheduled](https://learn.chatgpt.com/docs/automations?surface=web); saved files/connectors, temporary execution folders. |
   | Grok web | [Project](https://grok.com/project) + [Automation](https://grok.com/automations); verify scheduled project file access. |
   | Claude cloud chat | Project + [Cowork schedule](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork); writable account files/connectors. |
   | Claude Code cloud | [Claude Code Projects](https://code.claude.com/docs/en/claude-projects) + Library files + project memory + [project Routines](https://code.claude.com/docs/en/claude-projects#how-projects-relate-to-other-claude-code-features). |
   | OpenClaw | [Automations](https://docs.openclaw.ai/automation/cron-jobs) + owning agent's [workspace](https://docs.openclaw.ai/concepts/agent-workspace); keep Gateway running; verify scheduled [sandbox write access](https://docs.openclaw.ai/gateway/sandboxing#workspace-access). |
   | Hermes Agent | [`cronjob`](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) with absolute `workdir`; keep its profile's gateway running and [backend storage](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools#terminal-backends) persistent. |
   | Local CLI, IDE, desktop | Durable folder + native AI task ([OpenAI](https://learn.chatgpt.com/docs/automations?surface=app), [Claude Code](https://code.claude.com/docs/en/desktop-scheduled-tasks)); local execution needs host/app running. [Grok Build loops](https://docs.x.ai/build/features/background-tasks) are temporary. |
   | Hosted agents | Native tasks/routines; persist repository/state beyond disposable checkouts. [Codex cloud](https://learn.chatgpt.com/docs/environments/cloud-environment), [Claude Routines](https://code.claude.com/docs/en/routines), [Grok Bot `/workspace`](https://docs.x.ai/grok-bot/computer-and-apps). |

2. Verify `plan.md`, `connection.md`, `connection.db`, and any scripts survive the
   current chat and remain readable/writable from later chats and scheduled runs,
   and that scheduled runs can open SQLite (Python's standard `sqlite3` module or
   the `sqlite3` command), use protected credentials through the recorded
   storage references and access methods, and control pause/resume.
   - Establish this from the runtime's official guidance and the current
     environment. The first scheduled run confirms access, and a failure there
     follows [recovery](run-and-recover.md#recover-from-an-error).
   - Check actual storage and workspace bindings/permissions against official
     guidance. Cloud Projects may use durable writable storage without a
     permanent local folder when `connection.db` persists there.
3. If persistence or any required access is unavailable or unverified, stop and
   resolve access on the current platform using the
   [user action rule](#resolve-the-current-decisions). Recheck before work;
   migration requires user choice.

## Start or resume the project

1. After the access check passes, resolve a dedicated persistent project for one
   broker account and one asset type, available to later chats and scheduled runs.
   - Honor selected locations; resume clear matches and ask when ambiguous.
   - Keep authoritative files, user plans, and secrets outside the skill
     repository and temporary chat storage.
2. Read or initialize the project files.
   - `plan.md` from the [plan template](plan-template.md): setup decisions and
     user settings. Authoritative for decisions.
   - `connection.md` from the [connection template](connection-template.md):
     runbook, broker facts, and a status view for the user.
   - `connection.db` following [operational data](run-and-recover.md#operational-data):
     authoritative for state that changes during runs.
   - Follow [protected credential storage](credentials.md#prepare-protected-access)
     for all setup secrets. Record only storage references and runtime access
     methods; exclude secret values from files and reports.
   - Adapt the outlines; they are neither fixed schemas nor transcripts.

- Maintain the resume point in `plan.md` as answers, findings, actions, or
  failures change.
  - Record the current phase, open decisions, last outcome, next action, and
    actual scheduler state.
  - Save external action intentions before execution and results afterward for
    interrupted chats to reconcile.
  - Keep decisions and useful summaries in `plan.md`; link the runbook, scripts,
    and `connection.db`.

## Resolve the current decisions

1. Research facts with tools and documentation; identify user choices.
   - Honor existing answers and authority; revisit only changed or unclear
     material decisions. Choose routine technical details.
2. Request required user actions in a separate response and end the turn.
   - Include no interview questions, even independent ones or questions through tools.
   - Give instructions, alternatives, and a completion signal.
   - Record the waiting point in an existing accessible `plan.md`; if no usable
     project exists, provide a non-secret handoff in chat without creating files.
     Resume questions after completion and successful verification.
   - Use these markers:
     - `👉 **Action — Short title:**` required action and completion signal.
     - `↪️ **Alternative:**` another supported method.
     - `➡️ **Next:**` what happens next.
3. Ask the current round together, with prerequisites settled.
   - Skip settled questions; let answers determine the next round.
   - Give options on consecutive lines and a recommendation per question:

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

   - `Recommended all` accepts recommendations in the current round.
4. Summarize settled decisions at transitions and explain the next step.
   - Keep questions, results, and notifications understandable; include technical
     details only when useful to decisions.

## Setup phases

### Access

- Complete the [access check](#check-platform-and-automation-access) and
  [project setup](#start-or-resume-the-project).

### Broker

1. Identify the broker and asset type. Research the
   [broker contract](broker-contract.md) and record findings in `connection.md`.
2. Present the access options found, with tradeoffs, and let the user choose.
3. Set up and verify AlphaInsider and broker [credentials](credentials.md).
4. List every account the access reaches: main, sub-accounts, and paper or
   sandbox accounts, plus whether the user can open a new sub-account.
   - Show each account's type, live or paper, asset support, value, and existing
     holdings.
   - Offer all of them. Recommend a sub-account over the main account, because
     the connection closes holdings outside its targets.
   - Record the choice in `plan.md`, then research the
     [account facts](broker-contract.md#account) for that account.

### Allocations

1. Help the user find, filter, and subscribe to strategies through the
   [API skill](https://api.alphainsider.com/skill.md).
   - Check the user's active subscriptions against the connection's asset type.
     Both free and paid strategies qualify, including paid stock strategies.
     Owned strategies also require an active subscription.
   - Subscribe on the user's behalf only with consent and where the API allows;
     send the user to the strategy page when payment or private access is needed.
2. Ask for allocation targets as percentages or dollars, following
   [baselines](rebalance-math.md#baselines).
3. Ask for [leverage](rebalance-math.md#leverage) `L`, a whole number up to the
   account's `L_max` (recommend `min(2, L_max)`), explaining that sleeve gains
   and losses are `L / 2` times the strategy's. Then ask for the fee and slippage
   reserves, whether to rebalance when the connection starts (recommend yes),
   whether to rebalance when a deposit or withdrawal is detected (recommend yes,
   so new cash is invested without waiting for the next strategy trade), and
   whether stopping closes positions (recommend leaving positions).
4. Confirm the account-wide scope: the first rebalance closes holdings outside
   the targets. Name the holdings that would close.

### Build

1. Write the runbook in `connection.md` and any broker scripts the agent finds
   useful; choose the structure that best fits the broker.
2. Initialize `connection.db` and the symbol map. Report symbols that cannot be
   mapped or held.
3. Complete a [dry run](run-and-recover.md#dry-run) and show the proposed orders.

### Activate

1. After the user reviews the dry run, record their agreement to go live before
   sending any orders. Offer a small live test trade and place it only if the
   user also approves that trade.
2. Ask for the polling cadence within what the scheduler supports, notification
   events and channels, and whether to enable self-healing (recommend on).
   Preselect `🚨` action-required and `🛠️` self-healed notifications.
3. Run the first rebalance if the user chose to rebalance on start, then
   [activate the schedule](#activate-the-schedule).
4. Hand off the connection status, project location, next scheduled run, and any
   required next action.

## Choose the next phase

1. In a separate response, summarize the completed phase and ask one next-step
   question.
   - Offer: continue to the next phase, revise this phase, or save and stop.
   - Use `❓ **Next step:** What would you like to do?`, lettered options, and
     `➡️ **Recommended:**` with a reason.
2. End the turn and wait for the choice; include no other questions or user actions.
3. Record the choice in `plan.md`, then enter that phase.
   - Choosing forward confirms the summary; require no separate agreement prompt.

## Activate the schedule

1. Recheck [platform and automation access](#check-platform-and-automation-access)
   for the actual project and task; verify pause/resume support.
   - Leave inactive only for an explicit user pause or concrete setup failure;
     preserve user/error pauses and explain the blocker.
2. Enable new schedules automatically for the next scheduled run during agreed setup.
   - Require no separate activation confirmation.
   - If creation returns a paused task, enable it during the same setup.
3. Clear only setup-created execution blocks and verify the task is active.
4. Record task identity and next run in `plan.md`.

## Modify, stop, or resume

1. Establish the user's intent and save the exact handoff in `plan.md`.
   - Record whether automation is still running; clarify an ambiguous stop
     request when existing automation would be affected.
2. For changes to running behavior, pause automation and coordinate with the
   run lock before changing files in use.
3. Apply the affected changes.
   - Revisit only affected decisions and record them in `plan.md`.
   - Allocation or leverage changes reset baselines and trigger a rebalance
     following [baselines](rebalance-math.md#baselines). Show the resulting
     complete allocation list; if it sums above 1, ask how to fit it.
   - Stopping follows the recorded close-on-stop choice; confirm before closing
     positions.
4. Resume only when user intent and verified project state permit it.
