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
Set **Phase** to Interviewing and change **Plan agreement** to Draft while
Stage 3 decisions remain open.

### Access gate

Follow `credentials.md`. First inspect persistent-project and non-prompt secret
access without asking a question. If no safe scheduled-runtime location exists,
record the blocker and do not collect a key. Otherwise, privately verify a
configured key or make a missing key the first standalone user action.

After access is available, verify the token, user ID, read-only discovery
permissions, account limits, eligible settings, and compatible owned targets.
Do not ask the user to approve these lookups. Give one exact credential action
when initial access is insufficient.

### Target choice

Follow `alphainsider-target.md`. Ask only the recommended new target versus the
actual compatible owned targets in the first round. Then settle the selected
branch's settings in dependent rounds. Do not ask hypothetical new-target
settings, silently change an existing target, or combine paid behavior with the
public/private decision.

### Implementation and automation choices

Follow `automation.md`. Recheck scheduled-project access and scheduler
capabilities, then map the agreed decision mode, cadence, timezone, and market
rules. Ask only about unresolved material behavior, cost, or permission choices.

When the design is settled, derive and verify the key's exact setup and runtime
permissions. Resolve missing access before agreement. Then ask self-healing and
notification questions in their dependency order, with enabled recommended for
both. Store private notification destinations through `credentials.md` and put
only safe configuration references in project documents.

Record the exact offline build, target creation or binding, any target update,
description, scheduler, notification check, and activation actions. Summarize
the fixed missed-run, overlap, normal-run, dry-run, market-availability, and
quiet-success safeguards without presenting them as project choices.

### Implementation agreement

Show one normalized summary of the target and its settings, implementation,
schedule, self-healing, notifications, every planned remote change, and future
paper-order authority. State clearly that an active schedule and later
user-triggered normal runs can submit plan-conforming AlphaInsider paper orders
without another prompt. Offer **Agree and build**, **Revise**, or **Stop**.

Agreement authorizes only the listed local and external actions. On agreement,
set **Plan agreement** to Agreed and **Phase** to Building implementation. Build
and pass all offline, order-free checks before `newStrategy`. If a new path,
permission, target action, or schedule identity becomes necessary, return the
affected plan to Draft and resolve it.

## Completion

Set **Phase** to Complete and **Highest completed outcome** to Automated
strategy only after:

- the implementation and docs conform to `plan.md`;
- offline plan-conformance tests pass;
- the AlphaInsider target and saved public ID validate;
- a new target has the agreed generated description, or an existing target's
  description is preserved unless an explicitly agreed update was applied;
- the scheduler is active for the next normal occurrence; and
- notification delivery has been attempted when enabled.

Keep **Plan agreement** Agreed and **Automation state** Active. Follow the
success handoff in `generated-project.md`. If any gate remains open, record the
highest completed outcome, blocker, and exact next step instead of claiming
success.
