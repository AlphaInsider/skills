# Project Contract

This contract owns the generated workspace, plan compatibility and migration,
project documentation, scheduled-run instructions, and outcome handoffs. Use
it from the phase that creates or changes the corresponding artifact. Project
selection itself lives in [start or resume](start-or-resume.md).

Sections are ranked by operational importance and apply independently when
their owning artifact or event appears.

## Maintain the plan contract

1. Use [plan template](plan-template.md) for every new project.
2. Keep **Current status** first so a new agent can find the safe resume point
   before reading phase detail.
3. Keep the numbered strategy, backtest, and implementation sections in
   workflow order.
4. Update fields under their owning section without duplicating a second
   editable source of truth.
5. Apply lifecycle and authority transitions from
   [workflow contracts](workflow-contracts.md).

Every plan must retain exactly one `# Strategy Plan` title, one `## Current
status` section, all current field labels, their documented enums, and an
inline current value. Existing projects with the former flat section layout
remain current when their fields and semantics are current. Do not migrate a
plan solely to rearrange headings.

## Create and maintain the workspace

1. Create this core layout in the selected dedicated project:

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

2. Add only the dependency and tool files required by the implementation.
3. Put scheduled-run instructions in `runtime/runbook.md`.
4. Keep project state, the shared lock, histories, notification records, repair
   journals, and repair snapshots under `runtime/`.
5. Use project-relative paths unless the native scheduler requires a stable
   external project identity.

- `.env` is conditional and is not part of initial project creation.
- Create project `.env` only through the protected helper after project-file
  storage is selected. Use hosted secure storage instead when scheduled runs
  cannot use project secrets safely.
- Keep safe variable names and examples in `.env.example`, never values.
- Ignore secrets, caches, temporary files, and repair snapshots as applicable.
- Never write a strategy project inside this installed skill.

## Prove durable automation access

1. Before activation, prove that future scheduled AI instances can read and
   write the same project and exact code revision.
2. Prove access to `plan.md`, strategy source, tests, backtest evidence, saved
   trading state, the shared lock, run history, and repair records.
3. Prove non-prompt access to the selected secret facility and required
   network operations.
4. Record the result, source, and checked time in `plan.md`.

If project planning is durable but scheduled access is not, preserve the
project and implementation. Record one exact technical blocker and the user or
platform action that can resolve it. Never substitute another scheduler or
storage service without review.

## Migrate an older plan schema

1. Read the existing plan, saved artifacts, safe status, and resource
   identities without opening `.env`.
2. Before changing `plan.md`, save its exact contents to a new timestamped
   `runtime/migrations/plan-before-schema-migration-YYYYMMDDTHHMMSSZ.md`.
3. Use current UTC time and a collision-safe suffix. Never overwrite a prior
   backup.
4. Reconstruct every current field with the least-authoritative value proved by
   the old plan and durable evidence.
5. Record the backup path, migration time, decisions preserved, ambiguities,
   and exact resume step in the migrated plan.
6. Retain the backup until explicit deletion selects it.

Apply these mappings in dependency order:

1. **Strategy confirmation**

   - Map an agreed strategy, or an old Plan, Backtest, or Automated strategy
     outcome, to Strategy status Confirmed.
   - Otherwise, use Draft.
   - For incomplete creation, return a previously confirmed strategy to Draft
     only at a current Define decision whose scheduler, session-policy,
     execution, or public-limit evidence is missing.

2. **Backtest choice and evidence**

   - Map an accepted backtest choice to Backtest choice Selected.
   - Map a declined choice to Backtest choice and status Skipped.
   - For a selected backtest, use Completed only when a verified Valid artifact
     matches the current strategy and backtest plan.
   - Use Authorized only when the old phase or last step proves that the
     reviewed backtest plan received build authority; otherwise use Draft.
   - Preserve an old unavailable finding and offer **Backtest Strategy** unless
     the user already chose implementation.
   - Use Highest completed outcome Backtest only for matching Valid evidence;
     otherwise use Strategy defined for a Confirmed strategy.

3. **AlphaInsider setup**

   - Map an old building or configuring setup phase to AlphaInsider setup
     status Authorized.
   - Use Active only after every current completion gate is freshly verified.
   - Preserve every external identity and partial result.

4. **Creation and runtime state**

   - Map an old Complete phase without verified active automation to Creation
     state Stopped and reconstruct its nonterminal Phase from the last completed
     step and exact resume point.
   - Derive Operational health from durable run history: Not active before
     activation, Ready for active automation with no operational run, Healthy
     after the latest plan-compliant run, or Degraded/Retrying after an
     unresolved run error.
   - Preserve the actual native Automation state.
   - If an older workflow automatically paused the task for an operational
     error, keep it Paused during migration, retain Degraded/Retrying, and give
     the user the native resume action. Never silently resume an external task.

5. **Former leverage field**

   - Translate the old leverage value into maximum strategy exposure without
     claiming a universal AlphaInsider limit.
   - Preserve the value, mark execution-specific validation unresolved, and map
     the intended behavior to the current order operation.

Never promote ambiguous work to Authorized, Active, or Complete. Preserve
strategy decisions, historical evidence, safe resume data, and external
resources; do not repeat an action or create a sibling merely because the
schema changed.

Surface each material migration ambiguity in the next combined summary and
next-step prompt so the user can resolve it before dependent work.

A previously completed creation remains Complete when its current completion
gates verify. Unresolved runtime compatibility prevents a new order, keeps
active automation Degraded/Retrying, and uses next-trigger recovery instead of
rewriting creation history.

Creation state can first become Complete only when all of these are true:

- Phase is Complete.
- Strategy status is Confirmed.
- AlphaInsider setup status is Active.
- Highest completed outcome is Automated strategy.
- Automation state is Active.
- Operational health is Ready or Healthy.
- Every completion gate in
  [implement and activate](implement-and-activate.md) is verified.

A later operational error preserves Creation state and Phase Complete and
Automation state Active while setting health to Degraded/Retrying. A later user
pause also preserves completed creation but changes Automation state to Paused.
During incomplete creation, a user stop uses Stopped and a technical gate uses
Blocked; both retain the nonterminal Phase and exact resume step.

## Generate scheduled-run instructions

1. Save project-specific instructions in `runtime/runbook.md`.
2. Make them sufficient for a new scheduled AI instance with no chat history
   and no installed Strategy Creator skill.
3. Point to `plan.md` for confirmed strategy behavior; never duplicate a
   separately editable strategy specification.

Include:

- stable project identity, strategy-run and dry-run entries, decision
  responsibilities, exact commands, and hard risk limits;
- the shared lock, scheduled time, missed-run, overlap, compatibility,
  AlphaInsider strategy, documented-or-fallback session policy, expected
  closed-market skip, position, open-order, saved-state, duplicate, and
  structured-result rules;
- exactly one completed run per trigger and no faster-cadence polling,
  background loop, recursive scheduling, or host scheduler;
- the rule that an operational error ends order work for that trigger, leaves
  Automation state Active, sets Operational health to Degraded/Retrying, and
  retries checks on the next trigger;
- the order gate for unresolved or ambiguous results, no same-trigger order
  retry, no missed-order replay, and the complete repair, snapshot, rollback,
  and verified-recovery limits;
- every protected resource and the state, history, journal, snapshot, and
  report paths; and
- notification labels, selected events, independent channels, safe destination
  names, first-and-material-change deduplication, and best-effort delivery
  failure behavior.

Never put a secret in the runbook. Detailed runtime behavior comes from
[run and recover](run-and-recover.md); include its project-specific values,
not its generic interview procedure.

## Generate the project agent guide

Generated `AGENTS.md` must:

- make `plan.md` authoritative and route scheduled agents to
  `runtime/runbook.md`;
- require Strategy Creator for creation, updates, deletion, AlphaInsider
  strategy changes, and scheduler reconfiguration, but not for ordinary runs
  or confirmed self-healing;
- list the exact project test, backtest, and strategy-run commands, native task
  name, and safe configuration names;
- explain Creation state, Phase, Strategy status, Backtest status,
  AlphaInsider setup status, Highest completed outcome, Automation state, and
  Operational health;
- explain the shared lock and why user, update, deletion, or setup state pauses
  new orders while an operational error leaves automation Active and gates
  unsafe orders; and
- forbid secret exposure, opening or inspecting the complete `.env`, and
  orders during builds, tests, backtests, or dry runs.

Protect plan semantics, `pending-update.md`, AlphaInsider strategy identity and
settings, scheduler identity and frequency, credentials, saved trading history,
lock code, repair evidence, and protected tests from self-healing.

## Generate the human README

1. Write a concise project-specific README after the corresponding plan fields
   exist.
2. Update it whenever the confirmed plan, evidence, resources, or controls
   change.
3. Keep `plan.md` authoritative; do not create another editable strategy
   specification.

Include, ranked by operational importance:

- strategy purpose, strict stock or cryptocurrency type, assets, decision
  method, data, confirmed scheduler timing, mapped AlphaInsider operation and
  material side effects, execution-specific exposure, risk rules, and known
  limits;
- fixed-code, AI-decision, and code-and-AI responsibilities as applicable;
- safe configuration names and location, never values;
- whether the AlphaInsider paper strategy was created or reused, its name,
  simulated starting value, access setting, public strategy ID, and working
  link;
- scheduled task, frequency, timezone, daylight-saving behavior, next run,
  Automation state, Operational health, next retry when degraded, and history
  path;
- scheduler **Run now**, chat run, and chat dry-run controls, including that an
  order-capable run can submit plan-compliant paper orders without another
  prompt;
- self-heal settings, selected notification events and channels, each
  channel's supported or user-selected/unverified status, and whether
  notification repair is inside the confirmed repair scope;
- recovery, update, and explicit-deletion requests; and
- after creation completes, the stable broker-automation resource link.

For every backtest, include its exact command, future-information use,
differences, limitations, disposition, source snapshot or durable commit,
saved result visuals, and report. Feature the latest Valid result that matches
the current strategy, never the best-performing result. Retain recoverable
source until explicit deletion.

- Put the mandatory future-information warning before backtest results and
  beside every affected measurement when the answer is **Yes**.
- State that performance is not guaranteed and poor performance does not stop
  a strategy that follows the plan.
- Do not present direct terminal execution as the normal user control.
- For project `.env`, recommend active-chat entry first and direct editing
  second. Never expose the credential helper command.
- Never claim that a notification was delivered or tested during setup.
- Omit the broker resource until every creation gate passes.

## Hand off incomplete creation

1. Lead every user stop or technical creation blocker with **Creation
   incomplete**.
2. State the reason, current Phase, Strategy status, Highest completed outcome,
   project and plan locations, last completed action, exact resume step, and
   how to resume.
3. Inventory every relevant local and external resource, scheduled-task state,
   and whether scheduled runs and new orders are paused.
4. Add evidence appropriate to the highest completed phase.

- For a Draft or Confirmed strategy, summarize the strategy and open
  decisions.
- After backtesting, identify every run as `Backtest <date or ID> — Valid |
  Superseded | Failed`, with future-information use, differences, limitations,
  concise findings, disposition reason, report location, and the matching
  featured Valid result.
- During AlphaInsider setup, include the AlphaInsider strategy and link when
  assigned, all retained resource identities, and the exact setup resume point.

When presenting backtest findings, reuse the exact saved visuals for the
featured Valid run that matches the current strategy. Usually show the two to
four planned visuals. Embed them when supported; otherwise link directly to
each named image. A detailed report is additional, never a substitute. Include
an earlier diagnostic visual only when it materially helps. Keep every
future-information warning inside and beside the affected visual. If a planned
visual remains unavailable after its one safe rendering repair attempt, state
only that some planned visuals are unavailable and show the remaining findings
normally. A later repair uses the same saved output and preserves the original
failure record.

Do not use this handoff for an operational error after creation completed;
creation remains complete while run health becomes Degraded/Retrying. Do not
show the broker resource or ask another guided-creation question. A resume
instruction is sufficient.

## Hand off completed automation

1. Verify every completion gate in
   [implement and activate](implement-and-activate.md).
2. Use **Strategy created successfully** when the project created a new
   AlphaInsider strategy.
3. Use **Strategy automation completed successfully** when the project reused
   an existing AlphaInsider strategy.
4. Provide an informational handoff that asks for no approval.

Include the strategy and asset type, AlphaInsider settings and working link,
schedule and task, self-heal state, notification choices and support status,
project location, and any backtest findings, saved result visuals, and reports.
Apply the same evidence and warning rules as the incomplete handoff.

Then use the optional-next-step format from
[workflow contracts](workflow-contracts.md) with the short title **Connect a
broker**. Embed the current video when supported; otherwise link
[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades).
State that live broker mode can use real funds. Do not choose paper or live
broker mode, request broker credentials, create the connection, or ask another
guided-creation question.
