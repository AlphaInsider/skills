# Strategy Interview

Use this decision tree adaptively. Resolve dependencies before downstream
questions and skip branches that cannot affect the project.

## Protocol

- Ask exactly one decision question per turn and wait for the answer.
- Recommend one answer with a short reason. Record the user's answer, not the
  recommendation or conversation.
- Research repository, API, and provider facts instead of asking the user.
- Challenge lookahead, overfitting, unavailable data, timing mismatches,
  hidden cost, unreliable execution, and unnecessary complexity. Offer the
  simplest feasible alternative and resolve the choice.
- Update the matching plan section after every answer. Surface contradictions
  immediately rather than collecting incompatible requirements.
- Allow conservative defaults for incidental mechanics. Label them as agent
  defaults so the user accepts them with the complete plan.

## Decision tree

1. **Intent** — Establish the goal, hypothesis, intended behavior, evaluation
   horizon, and concrete success or failure criteria.
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
   restart state, disable conditions, logging, and recovery. For dynamic
   instruments, resolve validation freshness and whether one invalid candidate
   causes the cycle to continue with valid candidates or abort. Propose safe,
   simple defaults when the strategy does not require a special choice.
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
   historical window, evaluation timing, execution assumptions, costs, and
   metrics. Reuse production decision logic and implement only the smallest
   credible replay; signal-only evaluation is valid when portfolio accounting
   would be speculative.
9. **Implementation contract** — Resolve language when Python is unsuitable,
   module responsibilities, data flow, persistent state, configuration names,
   one-cycle and continuous commands, test scenarios, and acceptance criteria.
   Treat the selected project root as `.` in every persisted path; never embed
   machine-specific absolute paths or write generated artifacts into an
   installed skill directory.

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
