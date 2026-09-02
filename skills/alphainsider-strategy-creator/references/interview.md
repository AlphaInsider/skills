# Strategy Interview

Use the communication rules in `user-communication.md`. This interview is
dependency-aware: ask every available decision in the current round, record the
answers, then open the next dependent round. Skip irrelevant branches.

## Protocol

- Research project, market-data, storage, scheduler, and current applicable
  AlphaInsider constraints before offering choices. Ask the user only for
  intent, user-held facts, material choices, or required authority.
- Update `plan.md` after every answer and completed action. Set **Plan
  agreement** to Draft when an open decision can change intended behavior.
  For an active update, keep the current plan Agreed and mark
  `pending-update.md` Draft instead.
- Use conservative agent defaults for routine technical choices. Record each
  default, but do not make the user approve implementation trivia.
- Ask one normalized agreement question before executing each new stage. Do
  not add action-by-action approvals for work already listed in that agreed
  stage.
- Do not code a strategy while its applicable plan is Draft.
- If the user revises an earlier answer, keep unaffected decisions and reopen
  every dependent decision.
- If a technical discovery requires a high-level behavior change, explain the
  conflict and ask the affected strategy question again. Do not silently change
  the agreement to make code or a backtest work.

## Existing project

Read **Current status** and continue at **Next step** unless the user asks for
another supported action. Infer update, normal run, dry run, inspection, or
deletion from clear wording. Ask only when several projects or actions are
plausible.

For an update, use `changes-and-deletion.md`. If the new objective is a
different strategy, create a separate project. For deletion, use that reference
only after an explicit request.

## Stage 1: High-level strategy

Ask in this dependency order.

### Objective and market

1. What should the strategy do?
2. Will it trade stocks or cryptocurrency?
3. Which instruments can it select?
4. Is selection fixed, dynamic, or constrained dynamic?

Define a hard asset-type boundary. A cryptocurrency strategy cannot trade
stocks, and a stock strategy cannot trade cryptocurrency.

### Behavior and decision mode

Define inputs, transformations, signals, entries, exits, holding behavior,
tie-breakers, and missing-data behavior. Ask whether the strategy is:

- **code-led:** code applies fully specified rules;
- **agent-led:** each scheduled AI instance makes the decision; or
- **hybrid:** programs collect or calculate inputs and the scheduled AI makes
  a bounded decision.

For agent-led or hybrid behavior, define:

- the exact information the AI may use;
- the judgments it may make and decisions it may output;
- the allowed instrument set and risk limits;
- how it handles uncertainty, conflicting evidence, or invalid output; and
- what is a strategy decision versus a repairable implementation detail.

The scheduled AI can use its own reasoning. Do not require a separate model API
key unless the agreed strategy explicitly calls an external model service.

### Data, timing, execution, and risk

Research the smallest credible data stack. Resolve availability, timestamps,
freshness, licensing, cost, rate limits, and failure behavior. Ask only when a
cost, credential, scraping source, or material reliability tradeoff needs the
user's choice.

Define order method, sizing, positions, open orders, duplicate prevention,
reconciliation, loss controls, and maximum total exposure. Explain that
AlphaInsider permits up to `2×` leverage:

- `1×` means total exposure can equal the paper strategy value.
- `2×` means total exposure can be twice the paper strategy value.
- The selected value is a maximum, not a target.

Recommend `1×` unless the strategy and risk design support more. Never infer
`2×` from the platform limit.

Before asking cadence, inspect the current native AI scheduler's actual
interval, timezone, and market-hours options. Offer only supported schedules.
Record the exact timezone and daylight-saving-time behavior. If the requested
cadence is unsupported, explain the closest supported choices and ask the user
to select one.

### Strategy agreement

Show one concise normalized summary of the complete high-level strategy. Ask
whether to agree and continue, revise it, or stop with the plan. Recommend
agreement when no contradiction remains.

On agreement:

- set **Plan agreement** to Agreed;
- set **Highest completed outcome** to Plan;
- keep **Phase** at Interviewing until the backtest choice is made; and
- record the next step explicitly.

## Stage 2: Backtest choice and results

Determine historical feasibility before asking. Follow `backtesting.md`.
When a credible replay is possible, ask whether to backtest. Recommend yes.
When it is not possible, explain the missing history or reconstruction problem
and record Backtesting as unavailable.

If accepted, settle replay choices, ask agreement for the listed local build
and data access, then build and run it. Set **Phase** to Building backtest and
then Reviewing results. Show results and ask whether to keep the strategy,
revise it, or stop with the backtest. Never make profitability a pass/fail
gate. A plan-conforming strategy may continue with poor results.

After the results are settled, or after a declined/unavailable backtest, offer
AlphaInsider forward testing as the recommended next step.

If the user declines forward testing, set **Phase** to Complete and preserve
the Plan or Backtest outcome. Do not show the automated-strategy success
message.

## Stage 3: AlphaInsider and automation

Enter this stage only after the user chooses AlphaInsider forward testing.
Change **Phase** to Building implementation and **Plan agreement** to Draft
while new high-level implementation decisions remain.

Follow this order:

1. Recheck persistent project access from scheduled runs.
2. Follow `automation.md` to verify native scheduler capabilities.
3. Define code-led, agent-led, or hybrid runtime responsibilities.
4. Ask whether self-healing is enabled. Recommend enabled when the project has
   a safe plan-preserving repair scope.
5. Ask whether notifications are enabled. Recommend enabled. If enabled,
   discover supported channels and ask for the exact destination.
6. Follow `credentials.md` for the API key.
7. Follow `alphainsider-target.md` to show compatible owned targets and the
   recommended new-target option.
8. Record the exact offline build, target, description, scheduler, notification
   check, and activation actions.

When complete, show one normalized implementation summary. State clearly that
an active schedule and later user-triggered normal runs can submit
plan-conforming AlphaInsider paper orders without another prompt. Ask whether
to agree and build, create or bind the target, and activate the listed native
AI schedule. Offer revise or stop as alternatives.

That agreement authorizes only the listed local and external actions. Build and
pass all offline, order-free checks before `newStrategy`. If a new path,
permission, target action, or schedule identity becomes necessary, return the
affected plan to Draft and resolve it.

## Completion

Set **Phase** to Complete and **Highest completed outcome** to Automated
strategy only after:

- the implementation and docs conform to `plan.md`;
- offline plan-conformance tests pass;
- the AlphaInsider target and saved public ID validate;
- its description is current;
- the scheduler is active for the next normal occurrence; and
- notification delivery has been attempted when enabled.

Keep **Plan agreement** Agreed and **Automation state** Active. Follow the
success handoff in `generated-project.md`. If any gate remains open, record the
highest completed outcome, blocker, and exact next step instead of claiming
success.
