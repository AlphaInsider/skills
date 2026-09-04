# Strategy Interview

Use [user communication](user-communication.md). This file owns the creation
journey, stage summaries, next-step choices, stop behavior, and completion
gates. Ask every available decision in the current round and skip irrelevant
branches.

## Protocol

- Research project, market-data, storage, the actual native scheduler, and
  current AlphaInsider constraints before the affected choices. During Define
  Strategy ask only for strategy intent, timing, user-held facts, and material
  behavior choices; defer credentials and setup decisions to implementation.
- Update `plan.md` after every answer and completed action. Keep **Strategy
  status** Draft while an open decision can change intended behavior. Keep a
  confirmed strategy unchanged while a later backtest or setup plan is Draft.
- Use conservative defaults for routine technical choices. Give concise
  progress updates after a build choice and interrupt only for a material
  decision or blocker.
- Filter recommendations through known scheduler, data, and AlphaInsider
  constraints first. Bundle dependent timing details into complete compatible
  choices. Explain a limitation and ask for a resolution only after the user
  requests a conflicting outcome; never ask how to handle a hypothetical
  failure of a compatible recommendation. Still disclose material constraints
  and side effects in the stage summary.
- End each decision stage with one summary and destination-specific next-step
  choices. A forward choice confirms or authorizes the displayed scope. Never
  add a separate agreement question.
- Do not build a backtest until **Backtest status** is Authorized. Do not build
  an implementation or change AlphaInsider until **AlphaInsider setup status**
  is Authorized.
- If the user revises an earlier answer, retain unaffected answers and reopen
  every dependent decision. Preserve all earlier backtest reports.
- If a discovery changes strategy behavior, permissions, schedule, or a
  planned AlphaInsider action, return the affected stage to Draft and review
  it again. Apply compatible mechanical fixes without reopening decisions.

## Existing project

Read **Current status** and continue at **Next step** unless the user requests
another supported action. Infer update, chat run, dry run, inspection, or
deletion from clear wording. Ask only when several projects or actions are
plausible.

Project selection and resumption are an automatic preflight, not another
user-facing creation stage. Use [persistent project](project-root.md). For an
update, use `changes-and-deletion.md`. A different strategy belongs in a new
project. Deletion starts only after an explicit request.

## Stop, blockers, and resume

The user can stop at any time. **Save and Stop** declines only further work; it
never deletes anything. If an external action cannot be interrupted, let only
that action resolve, verify its result, and then stop.

Never set **Phase** or **Creation state** to Complete for a stop or blocker.
Preserve the current nonterminal Phase and set Creation state to Stopped for a
user stop or Blocked for a technical gate. Record the reason, last completed
step, exact resume step, and what is waiting. Use the **Creation incomplete**
handoff in [generated project guidance](generated-project.md).

Waiting for an ordinary answer, a requested API key, or a supported
user-operated control is not a blocker. Keep Creation state In progress and
record the exact action under Waiting for. Use Blocked only when a technical,
access, or capability failure prevents the expected next action until it is
remediated. If the user chooses to stop instead, use Stopped.

- Before the Define Strategy summary, a stop preserves a Draft strategy.
- At that summary, **Save This Strategy and Stop** confirms the reviewed
  strategy and sets the highest completed outcome to Strategy defined.
- At a backtest-plan or setup-plan summary before authorization, Save and Stop
  preserves that stage as Draft and authorizes no build or external action.
- After a Valid backtest for the current strategy and backtest plan, preserve
  its future-information use, limitations, Completed status, results, and
  Backtest outcome. After a Failed run, preserve its Failed status and
  diagnostic artifacts without advancing that outcome.
- During partial AlphaInsider setup, retain and inventory every local and
  external resource. Pause any active native schedule and set project state to
  prevent new orders. Do not show the broker handoff.

On an explicit resume, set Creation state to In progress and continue from the
recorded safe checkpoint. Recheck applicable AlphaInsider limits, identity and
settings, scheduler state, persistent access, and secrets access. Reconcile an
ambiguous or partial external result before retrying; never create a duplicate.

## Stage 1: Define Strategy

Ask in this dependency order.

### Objective and market

1. What should the strategy do?
2. Will it trade stocks or cryptocurrency?
3. Which assets can it trade?
4. Will it always use the same assets, choose from a defined list, or choose
   any asset of the selected type?

Make the stock-or-cryptocurrency boundary explicit. One AlphaInsider strategy
cannot trade both types.

### Behavior and decisions

Define inputs, transformations, signals, entries, exits, holding behavior,
equal values, and unavailable or unreliable data. Present the decision method
as:

- **fixed code:** code applies the specified strategy;
- **AI decision:** each scheduled AI instance decides inside confirmed limits;
  or
- **code and AI:** programs prepare inputs and the scheduled AI makes a bounded
  decision.

For AI decision or code and AI, define allowed evidence, judgments, outputs,
assets, risk limits, uncertainty behavior, and the boundary between a strategy
change and an implementation repair. Do not require another model API key
unless the strategy explicitly uses an external model service.

### Data, execution, timing, and risk

Research the smallest credible data and tool set. Resolve availability,
timestamps, freshness, licensing, cost, rate limits, and failure behavior. Ask
before a paid source, new credential, scraping, or a material reliability
tradeoff.

Define order type and size, positions, open orders, duplicate prevention,
saved state, loss controls, and maximum gross and net exposure. Internally map
the intended behavior to the current documented AlphaInsider operation; do not
ask the user to choose an endpoint name. Record the operation, its sources and
checked time, and every material side effect before strategy review.

Use execution-specific exposure rules:

- direct `newOrder` has no leverage field and no documented universal `2×`
  request ceiling; plan the user's exposure limit and defer current
  account/position-specific size verification to `getMaxOrderSize` in Stage 3;
- `newOrderAllocations` uses a complete target set, documents target and total
  allocation limits up to `2×`, cancels existing open orders, and closes
  positions omitted from the request; explain those cancellation and closure
  effects plainly before confirming an allocation design. Its current docs
  conflict on whether generated orders are market or limit orders; record that
  difference and do not confirm behavior that depends on one until clarified;
  and
- `newOrderWebhook` has its own `leverage` range up to `2×`, defaults to `1×`,
  and cancels existing open orders. Use it only when signal-style webhook
  behavior is actually intended.

Recommend exposure no greater than `1×` of strategy value as the conservative
risk choice when it fits the mapped operation, but describe it as the strategy
limit rather than a universal API default. When focused operation prose is
stricter than OpenAPI, follow the compatible prose and record the discrepancy.
For example, direct `newOrder` requires exactly one of `amount` or `total` even
though the current request schema does not encode that exclusive requirement.

Apply a public tier limit only to the operation its documentation names. If
the maximum planned calls per run and runs per day require a specific tier for
that operation, explain and record the minimum documented tier dependency
without asking for a key or the user's account tier. Verify the actual tier
only in Stage 3.

Before asking timing questions, follow the Define-time capability discovery in
[native AI automation](automation.md). Ask for the strategy's intended
decision time, useful frequency, timezone, daylight-saving behavior, and
data cutoff only through complete timing choices within the discovered
scheduler and AlphaInsider session policy. Each choice must combine the
cadence, run time, timezone, daylight-saving behavior, completed-data cutoff,
and order window that must work together. When required data becomes final
outside an accepted order window, recommend a later accepted run using the
latest completed data instead of asking about submission during an invalid
window.

If the user requests incompatible timing, explain the exact conflict and offer
only complete supported alternatives. A separate compute and execution design
is an option only when the native scheduler supports both triggers and the
result still forms one complete automation. Never offer submission with an
expected rejection, flattening after rejection, or a saved signal with no
supported execution time. Never use a long-running loop, poller, background
process, or host scheduler to simulate a faster cadence.

For stocks, dynamically verify which sessions accept the mapped order
operation from the installed `alphainsider-api` guidance and current live
focused docs and OpenAPI. An explicit current rule is authoritative. Do not
infer eligibility from a status name or example. When no explicit mapping is
published, use the Strategy Creator fallback for every AlphaInsider stock:
09:30 until, but not including, 16:00 `America/New_York` on a U.S. stock-market
trading day, including its holiday and early-close calendar. Record that this
is a fallback, not a claim from the API contract. A fixed-time recommendation
must sit comfortably inside that window under the discovered scheduler.

Treat AlphaInsider cryptocurrency order availability as 24/7. Do not ask a
market-session question for cryptocurrency, but still resolve scheduler
availability, the data source's candle or period boundary, its timezone, and
the delay before completed data is usable.

Explicit future AlphaInsider session guidance replaces the fallback for every
new or revised schedule. Newly supported hours become compatible choices but
never silently change an already confirmed schedule. If current guidance makes
a confirmed time invalid, reopen only the affected timing decision. Stage 3
rechecks a confirmed schedule; it does not select one for the first time.

### Review and choose the next step

Show one concise strategy summary only after the scheduler surface, feasible
cadence, mapped AlphaInsider operation, material side effects, applicable
public limits, and documented-or-fallback session policy are resolved. Include
those findings and the source or fallback in plain language without adding a
hypothetical failure question. Offer:

- **Backtest Strategy** — recommended; confirms the strategy and enters
  backtest feasibility and planning. Always show this choice and do not
  assess feasibility before the user selects it.
- **Skip Backtesting and Implement on AlphaInsider** — confirms the strategy
  and continues to API access, paper-strategy setup, implementation, and
  automation.
- **Revise Strategy** — returns to affected questions.
- **Save This Strategy and Stop** — confirms and saves the strategy while
  creation remains incomplete.

Any choice except Revise sets Strategy status to Confirmed and the highest
completed outcome to Strategy defined. Backtest Strategy sets Backtest choice
to Selected, Phase to Assessing backtest, and continues to Stage 2. Skip sets
Backtest choice and status to Skipped, Phase to Planning implementation, and
continues to Stage 3. Save sets Creation state to Stopped and uses the
incomplete handoff.

## Stage 2: Backtest Strategy

Enter only after the user selects Backtest Strategy. Follow
[backtesting](backtesting.md). Set Backtest status to Draft and Phase to
Assessing backtest. When an approach is ready to plan, set Phase to Planning
backtest.

### Assess feasibility

Assess feasibility before asking backtest-design questions. If a faithful
strategy backtest is straightforward, state that finding and continue directly
to the questions without another confirmation.

Use the confirmed implementable scheduler cadence and AlphaInsider execution
behavior for the primary backtest. For a backtest that substitutes a different
cadence or operation, record that exact difference and whether it uses
information unavailable at the historical decision time. Do not make an
unsupported higher-frequency backtest look like evidence for the scheduled
implementation.

If the backtest has material limitations, explain them before results can
anchor the user, recommend the most informative method, and let the user choose
or suggest any safe, technically possible, order-free backtest. A disclaimer
permits an imperfect user-directed backtest; it never permits undisclosed
future information, false claims, unauthorized data access, or an order. Set
**Uses information unavailable at the historical decision time** to **Yes** or
**No** before authorization and record every difference from intended
automated execution and other limitation. **Yes** requires a warning that the
backtest cannot demonstrate real-time strategy performance. When no proposed
method can run, explain the exact data or technical blocker and offer revision,
implementation without a backtest, or Save and Stop. Implementation without a
backtest sets Backtest choice and status to Skipped and enters Stage 3. Save
and Stop keeps the assessed backtest Draft and creation incomplete.

### Plan, review, and choose the next step

Settle the backtest period, data, decision and execution times, simulated value,
exposure, fills, fees, slippage, delay, missing data, comparison investment,
results, exact planned result visuals, and correctness checks. Normally plan two
to four data-derived visuals. Use equity against the comparison investment and
drawdown for portfolio results; put two suitable substitutes in a signal-only
plan that cannot honestly produce those views. Ask before paid data,
credentials, or scraping.

Show the complete backtest plan, future-information answer, required upfront
warning, known or expected differences from intended automated execution,
other limitations, unresolved implementation-dependent differences, data
access, and planned local work. Omit the future-information warning only when
the answer is **No**. Offer:

- **Build and Run** — authorizes only the displayed local build and data access;
- **Revise the Backtest** — returns to affected backtest questions;
- **Skip Backtesting and Implement on AlphaInsider** — marks the backtest
  Skipped and continues to Stage 3; or
- **Save and Stop** — saves the Draft backtest plan without authorizing it.

Build and Run sets Backtest status to Authorized and Phase to Building
backtest. Build and run the backtest, preserving every run and its inputs,
future-information answer, differences, limitations, disposition, assumptions,
changes, recoverable source, results, and artifacts. Then set Phase to
Reviewing results. A Valid run that matches the current strategy sets Backtest
status to Completed and highest completed outcome to Backtest. A Failed run
sets Backtest status to Failed only when no Valid run matches the current
strategy; otherwise keep Completed. A failure or evidence for a different
strategy never advances the highest completed outcome. Disclosed
future-information use or a backtest-only substitute does not prevent
completion unless it changes the intended strategy rather than approximating
it for the backtest.

### Review results and choose the next step

Identify each run as `Backtest <date or ID> — Valid | Superseded | Failed` and
state whether it used information unavailable at the historical decision time.
When it did, lead with the mandatory warning that the backtest cannot
demonstrate real-time strategy performance and repeat it beside affected
measurements. Put all material differences and disclaimers before headline
results and beside affected measurements. State each run's disposition and
reason. Feature the latest Valid run that matches the current strategy and list
every earlier, Superseded, and Failed backtest with its limitations. Performance
is information and never a pass/fail gate.

Include the featured run's exact saved result visuals in this results summary,
not only a link to its detailed report. Embed the images when supported;
otherwise link directly to each named image. Reuse those artifacts in every
later creation handoff that presents the findings. Show an earlier,
Superseded, or Failed run's diagnostic visual only when useful. If a planned
visual remains unavailable after the safe repair attempt in
[backtesting](backtesting.md), state only that some planned visuals are
unavailable; the rendering failure alone does not invalidate otherwise
trustworthy evidence.

Offer:

- **Implement Strategy on AlphaInsider** — continues to API access, paper
  strategy selection, implementation, and automation;
- **Correct and Rerun the Backtest** — applies a displayed mechanical
  correction inside the same backtest plan, or returns to the backtest
  questions when the plan must change, while preserving earlier runs;
- **Revise Strategy and Retest** — returns to affected Stage 1 decisions and
  supersedes affected evidence and invalidates dependent authorization without
  deleting evidence; or
- **Save and Stop** — saves the completed evidence while creation remains
  incomplete.

Choosing implementation keeps Completed when a Valid run matches the current
strategy and backtest plan and keeps Failed when none does. Preserve every
attempted run in either case.

Before a strategy or backtest-plan revision, mark each affected Valid run
Superseded with the exact reason and preserve its source, configuration, and
artifacts. If no other Valid run matches the revised current strategy and
backtest plan, clear the featured result, set the affected backtest plan to
Draft, and return Highest completed outcome to Strategy defined. A later Valid
run can advance it to Backtest again.

Show any known mechanical correction with the results. Choosing Correct and
Rerun authorizes only that displayed correction and rerun, sets Backtest status
to Authorized, and sets Phase to Building backtest. If the correction changes
the backtest plan or strategy, set the affected status to Draft and return to
its summary; do not rerun until the applicable forward choice is made.

## Stage 3: Implement Strategy on AlphaInsider

Enter after the user skips backtesting or selects implementation from results.
Set Phase to Planning implementation and AlphaInsider setup status to Draft.

### Access gate

Follow [credentials and configuration](credentials.md). First inspect project
and scheduled-run secret access for the native automation surface confirmed in
Stage 1. Recheck that surface and schedule automatically. If capability drift
would change strategy timing, return that decision to Draft in Stage 1. If no
safe secret location exists, record the technical blocker and do not collect a
key. Otherwise, privately verify configured access. Request a missing, invalid,
or inaccessible key as the first standalone AlphaInsider setup action; never
request a valid configured key again.

After access is available, verify the token, user ID, read-only discovery
permissions, current account tier, and applicable account-specific limits.
Resolve insufficient access before strategy discovery. If the account cannot
support a recorded higher-tier timing dependency, return the affected strategy
timing to Stage 1 rather than inventing an implementation workaround.

### AlphaInsider strategy choice

Follow [AlphaInsider strategy](alphainsider-strategy.md). Show the recommended
new paper strategy and actual compatible owned strategies. Reuse remains
allowed after disclosing attached history, subscribers, and a mismatched prior
purpose. Plan a new strategy or confirm exact reuse now; actual creation or
revalidation happens only after offline checks.

### Implementation and automation choices

Follow [native AI automation](automation.md). Recheck the selected native
automation surface's persistent access, scheduler capabilities, confirmed
timing, timezone, and current documented-or-fallback AlphaInsider session
policy. Do not ask the user to select timing here. When a supported schedule or
accepted stock session makes the confirmed timing unavailable, return the
affected timing to Stage 1 and later present a revised setup summary; never
select a replacement silently. Newly added compatible hours do not reopen or
silently change a valid confirmed schedule.

Map the confirmed fixed-code, AI-decision, or code-and-AI design. Derive and
verify exact setup and strategy-run permissions. Ask self-healing and
notification questions in dependency order, recommending enabled for both.
Automatic repair can change implementation details only, never strategy
behavior in response to performance.

Discover notification support without sending a test notification. Ask the
user to change a known unsupported selection. Accept a selection that cannot
be verified without delivery as user-selected and unverified. Notification
delivery is best effort during operation and never a creation or trading stop.

Compare the final data, decision, sizing, and execution design with every
backtest. Resolve previously unknown differences, update their reports
and `plan.md` disclosures without rewriting results, and show any material new
difference in the setup summary. Offer a new backtest when it would be useful,
but do not make performance or another backtest an implementation gate.

### Review AlphaInsider setup and choose the next step

Show the paper strategy choice and settings, implementation, schedule,
self-healing and whether notification repair is in scope, notifications and
support status, every planned AlphaInsider change, and future paper-order
authority. Offer:

- **Build, Configure, and Activate** — authorizes the listed local and external
  actions, native scheduler activation, and later scheduled or user-triggered
  paper orders that follow the confirmed strategy without another prompt;
- **Revise Setup** — returns to affected setup questions; or
- **Save and Stop** — saves the Draft setup without authorizing actions.

On Build, Configure, and Activate:

1. Set AlphaInsider setup status to Authorized and Phase to Building
   implementation.
2. Follow [strategy implementation](implementation.md) and pass every offline,
   order-free check, including the dry-run path. Never place a verification
   order.
3. Follow [AlphaInsider strategy](alphainsider-strategy.md) to create or
   revalidate the exact planned strategy. Preserve a partial or ambiguous
   result and reconcile it before retrying.
4. Set Phase to Configuring automation and follow
   [native AI automation](automation.md) to activate the native schedule. When
   only the user can activate it, wait for the action and verify the result.

If an unplanned strategy, permission, schedule, or AlphaInsider change becomes
necessary, return the affected status to Draft and show a revised summary.

## Completion

Set Phase and Creation state to Complete, AlphaInsider setup status to Active,
Highest completed outcome to Automated strategy, and Automation state to
Active with Operational health Ready only after:

- implementation and generated documentation conform to `plan.md`;
- offline tests prove the complete order-capable and dry-run paths;
- the AlphaInsider strategy ID, ownership, type, settings, and link validate;
- a new strategy has the generated description, or an existing description is
  preserved unless its update was authorized; and
- the native scheduler is active for the next scheduled run.

Do not send a setup notification or require delivery verification. Record each
selected channel as supported or user-selected and unverified. A later
notification failure never pauses the strategy, schedule, or new orders by
itself.

Only now use the adaptive success handoff in
[generated project guidance](generated-project.md): **Strategy created
successfully** for a newly created AlphaInsider strategy, or **Strategy
automation completed successfully** when an existing AlphaInsider strategy was
reused. It is informational and asks for no approval. If any gate remains open,
use Creation incomplete with the exact blocker and resume step instead.
