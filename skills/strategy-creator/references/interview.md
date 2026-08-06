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
  the user can accept or adjust instead of asking them to invent an answer from
  scratch.
- Research repository, API, and provider facts instead of asking the user.
- Challenge lookahead, overfitting, unavailable data, timing mismatches,
  hidden cost, unreliable execution, and unnecessary complexity. Offer the
  simplest feasible alternative and resolve the choice.
- Update the matching active plan section after every answer: `docs/plan.md`
  for a new or updated strategy and `docs/replacement-plan.md` for a staged
  replacement. Surface contradictions immediately rather than collecting
  incompatible requirements. Preserve `contract_version` until the versioning
  workflow authorizes advancing it.
- Allow conservative defaults for incidental mechanics. Label them as agent
  defaults so the user accepts them with the complete plan.
- Treat API-key permissions, owned-strategy discovery, eligibility, account
  limits, and endpoint fields as discoverable facts. Follow
  `alphainsider-target.md` and the credential gate in `SKILL.md` rather than
  asking the user to find IDs, scopes, or account details.

## Existing project branch

After preflight recognizes and checks a project under `versioning.md`, ask
exactly one question:
"Would you like to update the existing plan or replace the trading strategy
with a new one?" Present those as two short choices and recommend updating
because it preserves prior decisions.

- For **update**, preserve unaffected decisions and interview only the choices
  the requested change affects. For an older project, first complete the
  direct target audit and exact-path approval in `versioning.md`. Return a
  `confirmed` or `implemented` plan to `draft` before recording
  behavior-affecting gaps; do not interview for a documentation-only gap.
- For **replace**, leave the current plan and implementation untouched. Create
  or resume `docs/replacement-plan.md` on the installed version and run the
  complete decision tree for the new strategy. Do not upgrade the outgoing
  strategy. A confirmed replacement plan proceeds only to the separate
  deletion-approval gate in `SKILL.md`; it does not authorize deletion, plan
  promotion, or implementation.

If a valid replacement plan is already `draft`, resume its next unresolved
decision. If it is `confirmed`, proceed to the deletion inventory and approval
instead of repeating the interview.

## AlphaInsider target branch

After the API-key permission gate in `alphainsider-target.md`, resolve the
target before instrument selection:

- If a configured strategy validates, record `selected existing` and its
  strict asset class without recording the ID.
- If no strategy ID is configured, discover the authenticated user's owned
  strategies. Ask the user to select one or explicitly choose a new strategy;
  never choose the first result or create a duplicate silently. Persist an
  approved selection through the non-echoing helper and record `selected
  existing` without its ID.
- For a new target, first resolve the asset class. Propose a short name from the
  goal, require the user to choose the owner starting balance, and use the
  verified account checks in `alphainsider-target.md` to offer only eligible
  access modes.
  Present the exact type, name, starting balance, access, and launch price when
  applicable, then obtain explicit core creation approval while the plan is
  draft. If any core field later changes, invalidate and repeat that approval.
- Do not call `newStrategy` while the plan is draft. Generate the exact remote
  description after the behavior decisions are complete; its approval is part
  of final plan confirmation.

## Decision tree

1. **Intent** — Ask "What do you want this strategy to do?" and record the
   answer as the strategy goal.
2. **AlphaInsider target** — Resolve or provision the plan's `stock` or
   `cryptocurrency` target through the branch above, then choose an
   instrument-selection mode:
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
5. **Execution** — Resolve fixed versus allocation orders, types, sizing,
   entries, reductions, exits, and position/open-order reconciliation; apply
   the sibling AlphaInsider skill's normalized sizing/order rules. For
   allocations or webhook leverage, ask a separate maximum-exposure question:
   100% is 1× portfolio value, while AlphaInsider permits up to 200% (2×).
   Treat 200% as the platform ceiling, not a default; do not assume 100% is the
   platform maximum. Record the user's chosen cap under sizing and exposure
   constraints. Buying power, fees, and slippage may lower executable exposure.
   Use `getMaxOrderSize` as the fixed-order authority.
6. **Risk and operations** — Resolve position/exposure limits, stops or exit
   constraints, missing/stale data behavior, retries, duplicate events,
   restart state, automatic pause or shutdown conditions, logging, and
   recovery. For dynamic instruments, resolve validation freshness and whether
   one invalid candidate causes the cycle to continue with valid candidates or
   abort. Propose safe, simple defaults when the strategy does not require a
   special choice.
7. **Resources** — Derive technical requirements before selecting tools.
   Research current primary documentation for plausible sources and libraries;
   check coverage, history, timestamps, latency, authentication, price, rate
   limits, licensing, reliability, and maintenance burden. Recommend the
   smallest stack and record routine selections as agent defaults. Ask the user
   only when cost, credentials, scraping, or another meaningful tradeoff needs
   approval. Prefer AlphaInsider's applicable stock REST endpoints and
   `wsStockPrice` for supported current instrument metadata, exchange status,
   and bid, ask, or last prices when their coverage, freshness, and cadence fit.
   Use an external provider when AlphaInsider does not supply the required live
   market, cadence, freshness, or signal-specific input. For historical inputs
   used by live operation, compare AlphaInsider and external sources case by
   case under the same research criteria. Use scraping only with explicit
   approval, permitted access, no suitable supported feed, and a documented
   failure/maintenance plan.
8. **Backtesting** — Determine whether every signal input and decision timestamp
   can be reconstructed without future information. For dynamic selection,
   require the historical candidate set and selection inputs as they existed at
   each decision time; reject current-universe substitution and survivorship
   bias. Never use AlphaInsider's `getStockPriceHistory` for a backtest. Require
   a credible external historical source; if none is feasible, record the
   reason, mark backtesting unavailable, and do not offer it. If replay is
   otherwise feasible, always ask whether to backtest, then resolve the
   historical window, when results are measured, execution assumptions, costs,
   and results to report. Reuse production decision logic and implement only
   the smallest credible replay; signal-only evaluation is valid when portfolio
   accounting would be speculative. When production and replay use different
   providers, normalize them to the same decision-logic input contract and
   document timestamp, symbol, price-adjustment, and coverage differences.
9. **Implementation contract** — Resolve language when Python is unsuitable,
   module responsibilities, data flow, persistent state, configuration names,
   one-cycle and continuous commands, tests to run, and expected results.
   Select routine implementation details as agent defaults; ask the user only
   when a material tradeoff requires their decision.
   Require the generated README's short startup sequence to use those exact
   language-specific setup and run commands; for Python, include
   `source .venv/bin/activate` before the run choices.
   Treat the selected project root as `.` in every persisted path; never embed
   machine-specific absolute paths or write generated artifacts into an
   installed skill directory.
10. **Remote description** — Draft one to three plain-language sentences from
    the completed plan. Cover the traded universe, signal and entry/exit
    behavior, cadence, and sizing or risk without performance claims,
    credentials, implementation paths, or unsupported promises. Record the
    exact text and require synchronization before the plan can become
    `implemented`.

## Missing environment values

A missing API key or other required credential is a setup gap, not a strategy
decision. Pause the interview and follow **Environment setup** in `SKILL.md`.
Name the missing variables and exact project `.env` path, then recommend that
the user add the values there themselves and tell you when ready. If the user
wants agent-assisted entry, they may paste values in chat so you can add them.
Always warn first that pasting credentials is less secure because each value is
visible to the agent. A missing `ALPHAINSIDER_STRATEGY_ID` follows the target
branch above instead of being treated as a credential gap.

For pasted values, run `scripts/set_env_value.py` from the project root once per
variable and provide each value only through its non-echoing prompt. Never pass
a credential in a command argument, open `.env`, repeat a value, or put one in a
plan. Resume the interview only after the relevant non-ordering validation
succeeds; use the sibling request helper for AlphaInsider strategy
configuration.

## Confirmation gate

Before presenting the plan for confirmation:

- Verify the documented API-permission bundle. For an existing target, verify
  its ownership and type through the sibling request helper without reading or
  exposing `.env`. For a new target, require approved core creation fields and
  successful capacity and access checks, but do not create it yet.
- If the user explicitly named instruments, verify their mappings through the
  read-only stock lookup workflow. Otherwise ensure the plan defines runtime
  lookup, asset-class validation, freshness, and failure behavior.
- Ensure the selected data and library stack is available and obtain approval
  for any cost, credentials, scraping, or other material tradeoff.
- Ensure no implementation-blocking placeholder or contradiction remains.
- Include the exact generated AlphaInsider description. Plan confirmation
  authorizes its initial creation value and later synchronization after
  implementation verification.
- For an upgrade, ensure the installed target contract and its applicable tests
  conform before advancing `contract_version`; never advance to a remote
  version that this installed skill does not contain.
- State backtesting as unavailable, declined, or accepted with its exact scope.
- Present the complete normalized plan, including every agent default, and ask
  for explicit confirmation.
- For a replacement, do not combine plan confirmation with deletion approval.
  Leave the current plan and code unchanged until the user separately approves
  the exact deletion list and replacement-plan promotion.
