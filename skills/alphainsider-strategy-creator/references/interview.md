# Strategy Interview

Use [user communication](user-communication.md). This file owns the creation
sequence, agreements, status transitions, stop behavior, and completion gates.
Ask every available decision in the current round, then open the next
dependent round. Skip irrelevant branches.

## Protocol

- Research project, market-data, storage, scheduler, and current AlphaInsider
  limits and requirements before offering choices. Ask the user only for
  intent, user-held facts, material choices, or required authority.
- Update `plan.md` after every answer and completed action. Set **Plan
  agreement** to Draft when an open decision can change intended behavior.
  For an active update, keep the current plan Agreed and mark
  `pending-update.md` Draft instead.
- Use conservative defaults for routine technical choices. Record them without
  asking the user to approve implementation trivia.
- Ask one concise agreement question before executing each new stage. Do not
  add action-by-action approvals for work already listed in that agreed stage.
- Do not code a strategy while its applicable plan is Draft.
- If the user revises an earlier answer, keep unaffected decisions and reopen
  every dependent decision.
- If a technical discovery requires a high-level behavior change, explain the
  conflict and ask the affected strategy question again. Do not silently change
  the agreement to make code or a backtest work.

## Existing project

Read **Current status** and continue at **Next step** unless the user asks for
another supported action. Infer update, chat run, dry run, inspection, or
deletion from clear wording. Ask only when several projects or actions are
plausible.

For an update, use `changes-and-deletion.md`. If the new objective is a
different strategy, create a separate project. Use its deletion flow only
after an explicit request.

## Stop and resume creation

**Skip** declines only the current optional activity and continues the
creation flow. **Stop** ends the current creation request. A stop never
authorizes deletion.

When the user stops, do not start another planned action. If an external action
has already started and cannot be interrupted, allow only that action to
resolve, verify its result, and then stop. Record status by the last valid
outcome. Use [generated project guidance](generated-project.md) and this mapping:

| Stop point | Phase | Agreement | Highest outcome | Handoff |
| --- | --- | --- | --- | --- |
| Before strategy agreement | Complete | Draft | None | **Plan saved**; say it remains a draft |
| After strategy agreement | Complete | Agreed | Plan | **Plan saved** |
| After a valid backtest | Complete | Agreed | Backtest | **Backtest complete** |
| After AlphaInsider setup agreement | Complete | Agreed | Preserve Plan or Backtest | **Setup stopped** |

For the last row, set **Automation state reason** to User.

If the AlphaInsider setup made the plan Draft and the user stops before its
agreement, record AlphaInsider setup as not configured and restore the
preserved strategy plan to Agreed.

For a stopped partial setup with an order-capable path, save in project state
that new orders are paused. Pause any active native schedule and set
**Automation state** to Paused. If no schedule exists, set it to Not configured.
Retain and inventory every created local and external resource. Report any
native pause action that only the user can complete. Do not show an
automated-success or broker handoff.

On a later explicit resume, set **Phase** to the activity being resumed and
continue from the recorded safe checkpoint. First recheck current AlphaInsider
limits and requirements, strategy identity and settings, and scheduler state.
Do not repeat a completed AlphaInsider or scheduler change unless its current
result is verified and repeating it cannot create a duplicate.

## Stage 1: High-level strategy

Ask in this dependency order.

### Objective and market

1. What should the strategy do?
2. Will it trade stocks or cryptocurrency?
3. Which assets can it trade?
4. Will it always use the same assets, choose from an agreed list, or choose
   any asset of the selected strategy type?

Make the stock-or-cryptocurrency limit explicit. A cryptocurrency strategy
cannot trade stocks, and a stock strategy cannot trade cryptocurrency.

### Behavior and how decisions are made

Define inputs, transformations, signals, entries, exits, holding behavior,
what happens when values are equal, and what happens when data is unavailable
or unreliable. Record the user-facing choice in `plan.md`. Map it internally
to code-led, agent-led, or hybrid. Present the choices as:

- **fixed code:** code applies the fully specified strategy;
- **AI decision:** each scheduled AI instance decides within agreed limits; or
- **code and AI:** programs collect or calculate inputs and the scheduled AI
  makes a bounded decision.

For agent-led or hybrid behavior, define:

- the exact information the AI may use;
- the judgments it may make and decisions it may output;
- the allowed assets and risk limits;
- how it handles uncertainty, conflicting evidence, or invalid output; and
- what is a strategy decision versus a repairable implementation detail.

The scheduled AI can use its own reasoning. Do not require a separate model API
key unless the agreed strategy explicitly calls an external model service.

### Data, timing, execution, and risk

Research the smallest credible set of data sources and tools. Resolve
availability, timestamps, freshness, licensing, cost, rate limits, and failure
behavior. Ask only when a cost, credential, scraping source, or important
reliability tradeoff needs the user's choice.

Define order type and size, positions, open orders, duplicate prevention,
checks against saved position and order state, loss controls, and the maximum
total value of positions. Explain that AlphaInsider permits up to `2×`
leverage:

- `1×` means the total value of positions can equal the simulated strategy
  value.
- `2×` means the total value of positions can be twice the simulated strategy
  value.
- The selected value is a maximum, not a goal.

Recommend `1×` unless the strategy and risk design support more. Never infer
`2×` from the platform limit.

Before asking schedule frequency, inspect the current native AI scheduler's
actual interval, timezone, and market-hours options. Offer only supported
schedules. Record the exact timezone and daylight-saving-time behavior. If the
requested frequency is unsupported, explain the closest supported choices and
ask the user to select one.

### Strategy agreement

Show one concise summary of the complete high-level strategy. Ask whether to
**Agree to this strategy**, **Revise**, or **Stop**. Recommend agreement when
no contradiction remains. Do not mention backtesting in this agreement
question, its choices, or its recommendation.

On agreement:

- set **Plan agreement** to Agreed;
- set **Highest completed outcome** to Plan;
- keep **Phase** at Interviewing until the backtest choice is made; and
- record the next step explicitly.

## Stage 2: Backtest choice and results

After strategy agreement, determine whether the strategy can be backtested
reliably before the next user question. Follow [backtesting](backtesting.md).
When a credible backtest is possible, briefly explain its important limits and
ask directly whether the user wants to **Backtest this strategy**, **Skip the
backtest**, or **Stop**. Recommend the backtest. Do not preview this choice in
the strategy-agreement block. When a credible backtest is not possible,
explain why past decisions cannot be recreated reliably, record Backtesting as
unavailable, and do not offer an unavailable choice.

If accepted, settle backtest choices and show the concise backtest plan. Ask
whether to **Agree to this backtest plan**, **Revise**, or **Skip the
backtest**. State that agreement authorizes the listed local build and data
access. Then build and run it. Set **Phase** to Building backtest and then
Reviewing results. Show results and ask whether to **Keep this strategy**,
**Revise**, or **Stop**. Do not mention AlphaInsider in this question, its
choices, or its recommendation. Never make profitability a pass/fail gate. A
strategy that follows the agreed plan may continue with poor results.

After the user keeps the strategy, after either backtest **Skip** choice, or
when a backtest is unavailable, separately ask whether to set up the strategy
on AlphaInsider. Briefly explain that it will use current market information
and simulated funds. Use only **Set up this strategy on AlphaInsider** and
**Finish here** as choices, and recommend setup.

If the user finishes here, set **Phase** to Complete and preserve the Plan or
Backtest outcome. Use the applicable Stop handoff above.

## Stage 3: AlphaInsider setup and automation

Enter this stage only after the user chooses to set up the strategy on
AlphaInsider. Set **Phase** to Interviewing and change **Plan agreement** to
Draft while Stage 3 decisions remain open.

### Access gate

Follow [credentials and configuration](credentials.md). First inspect project
access and secret access that does not require a person during each run. Do not
ask an interview question for this check. If no safe location is available to
scheduled runs, record the blocker and do not collect a key. Otherwise,
privately verify a configured key or make a missing key the first standalone
user action.

After access is available, verify the token, user ID, and read-only discovery
permissions. Do not ask the user to approve these checks. Give one exact
credential action when access is insufficient; AlphaInsider strategy discovery
starts only after this gate passes.

### AlphaInsider strategy choice

Follow [AlphaInsider strategy](alphainsider-strategy.md). Ask only the
recommended new AlphaInsider strategy versus the actual compatible owned
strategies in the first round. Then settle the selected branch's settings in
dependent rounds. Do not ask hypothetical new-strategy settings, silently
change an existing AlphaInsider strategy, or combine paid access with the
public/private decision.

### Implementation and automation choices

Follow [native AI automation](automation.md). Recheck scheduled-project access
and scheduler capabilities, then map the agreed way decisions are made,
schedule, timezone, and market rules. Ask only about unresolved material
behavior, cost, or permission choices.

When the design is settled, derive and verify the key's exact setup and
strategy-run permissions. Resolve missing access before agreement. Then ask
self-healing and notification questions in their dependency order, with
enabled recommended for both. Store private notification destinations through
[credentials and configuration](credentials.md) and put only safe
configuration references in project documents.

Record the exact offline build, creation or use of the AlphaInsider strategy,
any agreed AlphaInsider change, description, scheduler, notification check, and
activation actions. Summarize the fixed missed-run, overlap, strategy run, dry
run, market-availability, and quiet-success safeguards without presenting them
as project choices.

### AlphaInsider setup agreement

Show one concise summary of the AlphaInsider strategy and its settings,
implementation, schedule, self-healing, notifications, every planned change on
AlphaInsider, and authority for future AlphaInsider paper orders. State clearly
that an active schedule and later user-triggered strategy runs can submit paper
orders that follow the agreed plan without another prompt. Offer **Agree to
this AlphaInsider setup**, **Revise**, or **Stop**. State that agreement
authorizes the listed local and external actions; do not put those later
actions in the option label.

Agreement authorizes only the listed local and external actions. On agreement:

1. Set **Plan agreement** to Agreed and **Phase** to Building implementation.
2. Follow [strategy implementation](implementation.md) and pass all offline,
   order-free checks against the
   [scheduled run process](scheduled-runs.md).
3. Follow [AlphaInsider strategy](alphainsider-strategy.md) to create or use and
   validate the agreed AlphaInsider strategy.
4. Set **Phase** to Configuring automation and follow
   [native AI automation](automation.md) to activate the agreed schedule.

If a new path, permission, AlphaInsider change, schedule identity, or behavior
becomes necessary, return the affected plan to Draft and resolve it before
continuing.

## Completion

Set **Phase** to Complete and **Highest completed outcome** to Automated
strategy only after:

- the implementation and docs conform to `plan.md`;
- offline tests prove the implementation follows `plan.md`;
- the AlphaInsider strategy and saved AlphaInsider strategy ID validate;
- a new AlphaInsider strategy has the agreed generated description, or an
  existing strategy's description is preserved unless an explicitly agreed
  update was applied;
- the scheduler is active for the next scheduled run; and
- notification delivery has been attempted when enabled.

Keep **Plan agreement** Agreed and **Automation state** Active. Follow the
success handoff in [generated project guidance](generated-project.md). If any
gate remains open, record the highest completed outcome, blocker, and exact
next step instead of claiming success.
