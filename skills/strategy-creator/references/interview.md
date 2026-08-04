# Strategy Interview

Use this decision tree adaptively. Resolve dependencies before downstream
questions and skip branches that cannot affect the project.

## Protocol

- Ask exactly one decision question per turn and wait for the answer.
- Recommend one answer with a short reason. Record the user's answer, not the
  recommendation or conversation.
- Use plain trading language for a user who understands profit, loss, fees,
  trades, and percentage limits. Avoid specialist terms when familiar words
  work. If a specialist term is necessary, explain it immediately; for
  example, describe drawdown as the largest drop from a previous high.
- Make each question easy to answer by including a brief example or two or
  three short choices. Use earlier answers to recommend a concrete choice that
  the user can accept or adjust instead of asking them to invent a measurement.
- Research repository, API, and provider facts instead of asking the user.
- Challenge lookahead, overfitting, unavailable data, timing mismatches,
  hidden cost, unreliable execution, and unnecessary complexity. Offer the
  simplest feasible alternative and resolve the choice.
- Update the matching active plan section after every answer: `docs/plan.md`
  for a new or updated strategy and `docs/replacement-plan.md` for a staged
  replacement. Surface contradictions immediately rather than collecting
  incompatible requirements.
- Allow conservative defaults for incidental mechanics. Label them as agent
  defaults so the user accepts them with the complete plan.

## Existing project branch

After preflight recognizes a project from the status, `# Strategy Plan` title,
and current template sections in `docs/plan.md`, ask exactly one question:
"Would you like to update the existing plan or replace the trading strategy
with a new one?" Present those as two short choices and recommend updating
because it preserves prior decisions.

- For **update**, preserve unaffected decisions and interview only the choices
  the requested change affects. Return a `confirmed` or `implemented` plan to
  `draft` before recording behavior changes.
- For **replace**, leave the current plan and implementation untouched. Create
  or resume `docs/replacement-plan.md` and run the complete decision tree for
  the new strategy. A confirmed replacement plan proceeds only to the separate
  deletion-approval gate in `SKILL.md`; it does not authorize deletion, plan
  promotion, or implementation.

If a valid replacement plan is already `draft`, resume its next unresolved
decision. If it is `confirmed`, proceed to the deletion inventory and approval
instead of repeating the interview.

## Decision tree

1. **Intent** — Ask these as separate questions, in order when each still
   applies:
   - "What do you want this strategy to do?"
   - "Why do you think this trading idea could work?"
   - "After how much time or how many trades should we review the results?"
   - "What results would tell you the strategy is working?"
   - "What loss or behavior would make you change or stop it?"

   Build the recommendation for each question from earlier answers. A concrete
   result might be "profitable after fees over 50 trades without the account
   falling more than 10% from a previous high." Treat these answers as a review
   of whether the trading idea is working; keep them separate from automatic
   safety limits and shutdown rules.
2. **AlphaInsider target** — Resolve the configured strategy's strict `stock`
   or `cryptocurrency` type, then choose an instrument-selection mode:
   `fixed`, `dynamic`, or `constrained dynamic`. For fixed selection, record
   explicitly named instruments and their mappings. For dynamic selection,
   define the runtime selector without requiring an advance list. For
   constrained dynamic selection, define the category, allowlist, or other
   boundary within which runtime selection may operate. Every traded candidate
   must match the configured asset class.
3. **Signals** — Define every input, transformation, entry decision, exit or
   holding rule, and tie-breaking behavior. Prefer deterministic rules. For an
   LLM or hosted model, additionally define the prompt/input contract, output
   schema, model expectations, cost ceiling, timeout, invalid-output handling,
   and fallback.
4. **Timing** — Resolve bar or event timing, polling or streaming, schedule,
   market-hours behavior, decision latency, late events, and when an order is
   evaluated relative to its signal.
5. **Execution** — Resolve fixed orders versus allocation rebalancing, order
   types, sizing units, entries, reductions, exits, and existing position/open
   order reconciliation. Apply the sibling AlphaInsider skill's normalized
   sizing and order rules.
6. **Risk and operations** — Resolve position/exposure limits, stops or exit
   constraints, missing/stale data behavior, retries, duplicate events,
   restart state, automatic pause or shutdown conditions, logging, and
   recovery. These are immediate safeguards, not the longer-term review of
   whether the strategy is working. For dynamic instruments, resolve validation
   freshness and whether one invalid candidate causes the cycle to continue
   with valid candidates or abort. Propose safe, simple defaults when the
   strategy does not require a special choice.
7. **Resources** — Derive technical requirements before selecting tools.
   Research current primary documentation for plausible sources and libraries;
   check coverage, history, timestamps, latency, authentication, price, rate
   limits, licensing, reliability, and maintenance burden. Recommend the
   smallest stack and obtain confirmation. Prefer Alpaca for equity data and
   Coinbase for cryptocurrency data when they fit. Use scraping only with
   explicit approval, permitted access, no suitable supported feed, and a
   documented failure/maintenance plan.
8. **Backtesting** — Determine whether every signal input and decision timestamp
   can be reconstructed without future information. For dynamic selection,
   require the historical candidate set and selection inputs as they existed at
   each decision time; reject current-universe substitution and survivorship
   bias. If replay is infeasible, record the reason and do not offer a
   misleading test. If feasible, ask whether to backtest, then resolve the
   historical window, when results are measured, execution assumptions, costs,
   and results to report. Reuse production decision logic and implement only
   the smallest credible replay; signal-only evaluation is valid when portfolio
   accounting would be speculative.
9. **Implementation contract** — Resolve language when Python is unsuitable,
   module responsibilities, data flow, persistent state, configuration names,
   one-cycle and continuous commands, tests to run, and expected results.
   Treat the selected project root as `.` in every persisted path; never embed
   machine-specific absolute paths or write generated artifacts into an
   installed skill directory.

## Missing environment values

A missing environment value is a setup gap, not a strategy decision. Pause the
interview and follow **Environment setup** in `SKILL.md`. Name the missing
variables and exact project `.env` path, then ask the user to either add the
values there and tell you when ready, or paste them in chat so you can add them.
Always warn that pasting credentials in chat is less secure.

For pasted values, run `scripts/set_env_value.py` from the project root once per
variable and provide each value only through its non-echoing prompt. Never open
`.env`, repeat a value, or put one in a plan or command argument. Resume the
interview only after the relevant non-ordering validation succeeds; use the
sibling request helper for AlphaInsider strategy configuration.

## Confirmation gate

Before presenting the plan for confirmation:

- Verify the `.env`-configured AlphaInsider strategy and its type through the
  sibling request helper without reading or exposing `.env`.
- If the user explicitly named instruments, verify their mappings through the
  read-only stock lookup workflow. Otherwise ensure the plan defines runtime
  lookup, asset-class validation, freshness, and failure behavior.
- Ensure the selected data and library stack is available and approved.
- Ensure no implementation-blocking placeholder or contradiction remains.
- State backtesting as unavailable, declined, or accepted with its exact scope.
- Present the complete normalized plan, including every agent default, and ask
  for explicit confirmation.
- For a replacement, do not combine plan confirmation with deletion approval.
  Leave the current plan and code unchanged until the user separately approves
  the exact deletion list and replacement-plan promotion.
