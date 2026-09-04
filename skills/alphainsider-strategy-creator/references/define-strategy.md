# Define Strategy

Use this workflow for a new strategy, an incomplete definition, or affected
strategy decisions reopened by an update or incompatible drift. It owns the
strategy interview, Define-time market and platform research, execution
mapping, timing design, and reviewed strategy handoff.

## 1. Enter definition

1. Set Phase to Defining strategy and keep Strategy status Draft while an open
   decision can change intended behavior.
2. Load existing answers from `plan.md`; ask only unanswered, revised, or newly
   dependent decisions.
3. Research project, market-data, native-scheduler, and public AlphaInsider
   facts before the questions they constrain.
4. Apply the rounds and authority rules in
   [workflow contracts](workflow-contracts.md).

During Define, ask only for strategy intent, timing intent, user-held facts,
and material behavior choices. Defer API keys, account facts, secret storage,
AlphaInsider strategy selection, self-healing, notifications, and other setup
decisions to [implement and activate](implement-and-activate.md).

Do not ask who will operate native controls or where secrets will live during
Define.

## 2. Define the objective and market

Ask these decisions in dependency order:

1. What should the strategy do?
2. Will it trade stocks or cryptocurrency?
3. Which assets can it trade?
4. Will it always use the same assets, choose within defined limits, or choose
   any asset of the selected type?

- Make the strict stock-or-cryptocurrency boundary explicit. One AlphaInsider
  strategy cannot trade both types.
- Define a fixed list as **fixed**, changes inside explicit limits as
  **constrained dynamic**, and unrestricted choice within the strict asset type
  as **dynamic**.
- Resolve the intended outcome without promising performance.

## 3. Define behavior and decision responsibility

1. Define required inputs and transformations.
2. Define signals and decision rules.
3. Define entry, exit, holding, and equal-value behavior.
4. Define missing, outdated, late, invalid, and conflicting-data behavior.
5. Choose one decision mode:

   - **Fixed code (code-led):** project code applies the specified strategy.
   - **AI decision (agent-led):** each scheduled AI instance decides inside
     confirmed limits.
   - **Code and AI (hybrid):** programs prepare or calculate inputs and enforce
     mechanical limits; scheduled AI makes only assigned judgments.

For agent-led or hybrid behavior, define:

- permitted evidence and its cutoff;
- allowed judgments, asset choices, and output shape;
- hard sizing, exposure, loss, and uncertainty limits;
- what the AI must do when evidence is insufficient or conflicting;
- the exact boundary between a strategy change and an implementation repair;
  and
- the division between code and AI for a hybrid design.

Do not require another model API key unless the strategy explicitly chooses an
external model service. The native scheduled AI can supply the confirmed
reasoning role.

## 4. Resolve data, execution, and risk

1. Research the smallest credible data and tool set.
2. Verify availability, timestamps, freshness, licensing, cost, rate limits,
   and failure behavior.
3. Ask before selecting a paid source, new credential, scraping, or material
   reliability tradeoff.
4. Define the required information, completed-data boundary, backup source, and
   behavior when data is unavailable or unreliable.
5. Define intended order behavior, size, positions, open orders, duplicate
   prevention, saved state, retries, loss controls, and maximum gross and net
   exposure.
6. Internally map the intent to the current documented AlphaInsider operation.
   Do not ask the user to choose an endpoint name.
7. Record the operation, sources, checked time, account-tier dependency, and
   every material side effect before review.

Apply the operation-specific rules below.

### Direct order

- `newOrder` has no leverage field and no documented universal `2×` request
  ceiling.
- Plan the user's exposure limit and defer current account- and
  position-specific size verification to `getMaxOrderSize` during
  implementation and every applicable run.
- Require exactly one of `amount` or `total`. Current focused prose is stricter
  than the request schema on this exclusive requirement; follow the prose and
  record the discrepancy.

### Complete target allocation

- `newOrderAllocations` sends a complete target set and documents target and
  total allocation limits up to `2×`.
- It cancels existing open orders and closes positions omitted from the
  request. Explain both effects plainly before confirming this design.
- Current documentation conflicts on whether generated orders are market or
  limit orders. Record the difference and do not confirm behavior that depends
  on one interpretation until authoritative guidance resolves it.

### Signal-style webhook

- `newOrderWebhook` has its own `leverage` range up to `2×`, defaults to `1×`,
  and cancels existing open orders.
- Use it only when signal-style webhook behavior is actually intended.

Recommend exposure no greater than `1×` of strategy value when it fits the
mapped operation. Describe this as the strategy's conservative limit, never as
a universal API default.

Apply a public account-tier limit only to an operation that its documentation
explicitly names. Calculate maximum planned calls per run and runs per day. If
the cadence has a documented minimum tier for the mapped operation, explain and
record the dependency without requesting a key or asking the user's tier.
Do not inspect the user's account tier during Define. Verify the actual account
only during implementation.

## 5. Discover native timing capabilities

Complete this discovery before asking timing questions.

1. Inspect the actual current platform's tools and official scheduler
   documentation. Do not assume web, desktop, and command-line products have
   the same controls.
2. Resolve the native surface without a user question when current context is
   clear.
3. Record the source, checked time, and these schedule-critical capabilities:

   - frequency limits and precision;
   - timezone and daylight-saving behavior;
   - missed-run and scheduler-retry behavior;
   - overlap, history, notification, and duration behavior;
   - whether one invocation can perform exactly one complete strategy run; and
   - whether the documented surface can ultimately create, inspect, edit,
     pause, resume, run now, and remove a task, including user-operated
     controls.

4. Resolve the current AlphaInsider accepted-session policy for the mapped
   operation.
5. Offer only complete timing choices that fit the scheduler, data boundary,
   and accepted order window.

Never simulate a faster cadence by keeping a scheduled run alive, sleeping,
polling, looping, recursively scheduling, or starting a background process.
Each trigger performs at most one complete strategy run and finishes. If the
native scheduler cannot provide a useful cadence, keep timing unresolved,
record the technical blocker, and preserve resumable Define state.

Never install or recommend cron, systemd, launchd, Windows Task Scheduler, a
daemon, or another host scheduler or background service.

### Stock session policy

1. Read installed `alphainsider-api` guidance and the current live `llms.txt`
   index.
2. Read any indexed session guidance, the focused `getExchangeStatus` and
   selected order-operation pages, and applicable OpenAPI operations.
3. Use an explicit current accepted-session rule when one is published. An
   exchange-status name or example value is not proof of permission.
4. When no source publishes an operation mapping, use the Strategy Creator
   fallback for every AlphaInsider stock: 09:30 until, but not including, 16:00
   `America/New_York` on a U.S. stock-market trading day, including holidays
   and early closes.
5. Record the missing mapping and identify the fallback as Strategy Creator
   policy, not API documentation.

A fixed-time recommendation must sit comfortably inside the applicable window
under the scheduler's precision and delay behavior. Explicit later guidance
replaces the fallback for a new or revised schedule. Added support does not
expand an already confirmed schedule; incompatible guidance reopens only the
affected timing decision.

### Cryptocurrency availability

- Treat AlphaInsider cryptocurrency order availability as 24/7.
- Do not ask a cryptocurrency market-session question.
- Still constrain timing by native scheduler support, the data source's candle
  or period boundary, its timezone, and the delay before completed data is
  usable.

## 6. Select complete timing behavior

1. Ask for intended decision time, useful frequency, timezone,
   daylight-saving behavior, data cutoff, and order window through bundled
   compatible choices.
2. When required data becomes final outside an accepted order window,
   recommend a later accepted run that uses the latest completed data.
3. If the requested cadence is unavailable, explain the exact conflict and
   offer the nearest complete supported alternatives.
4. Offer separate compute and execution triggers only when the native scheduler
   supports both and together they form one complete automation.
5. Record the selected schedule, timezone, daylight-saving behavior,
   documented-or-fallback session policy, surface, capability source, and
   checked time.

Never offer submission with an expected rejection, flattening after a rejected
action, or a saved signal without a supported execution time.

Use these implementation defaults unless the confirmed strategy needs another
supported choice:

- one strategy run per scheduler trigger;
- skip missed runs without catch-up;
- disable scheduler-level automatic retries;
- reject overlap with the project lock;
- keep healthy runs quiet; and
- activate for the next scheduled run without an order-capable setup run.

If native retries or catch-up cannot be disabled, record the limitation and
require scheduled-time and lock checks to reject stale or duplicate work. Every
run must also exit when project state says new orders are paused.

A stock trigger outside its confirmed window because of a holiday, early
close, or late start is an expected no-order result. Do not submit, flatten, or
carry a stale signal by default; the next trigger recomputes from current data.

## 7. Review the strategy and route forward

1. Confirm that every strategy field is resolved, including scheduler surface,
   feasible cadence, mapped AlphaInsider operation, material side effects,
   applicable public limits, and documented-or-fallback session policy.
2. Show one concise strategy summary with those findings and their source or
   fallback in plain language.
3. Offer these choices:

   - **Backtest Strategy** — recommended; confirms the strategy and enters
     feasibility assessment and planning. Always show this choice and never
     assess feasibility before the user selects it.
   - **Skip Backtesting and Implement on AlphaInsider** — confirms the strategy
     and enters paper-strategy setup, implementation, and automation.
   - **Revise Strategy** — returns to affected decisions.
   - **Save This Strategy and Stop** — confirms and saves the strategy while
     creation remains incomplete.

4. Apply the selected transition:

   - Any choice except Revise sets Strategy status Confirmed and Highest
     completed outcome Strategy defined.
   - Backtest Strategy sets Backtest choice Selected, Phase Assessing backtest,
     and continues to [backtest strategy](backtest-strategy.md).
   - Skip sets Backtest choice and status Skipped, Phase Planning
     implementation, and continues to
     [implement and activate](implement-and-activate.md).
   - Save sets Creation state Stopped and uses the incomplete handoff in
     [project contract](project-contract.md).
