# Strategy Interview

Use this design tree adaptively. Resolve dependencies before downstream
questions and skip branches that cannot affect the project.

## Contents

- [Protocol](#protocol)
- [Existing project](#existing-project)
- [Design tree](#design-tree)
- [Missing environment values](#missing-environment-values)
- [Confirmation gate](#confirmation-gate)

## Protocol

Interview in frontier rounds. Do not depend on any other skill for this
pacing.

- Research repository, API, host, and provider facts instead of asking the
  user.
- The frontier is every user decision whose prerequisites are already settled.
  Ask every currently unblocked user decision in one turn through the agent's
  interactive question prompt — the blocking multiple-choice question UI, not
  ordinary chat text. One prompt may contain the whole frontier. For each
  decision: a short question, two or three choices when that fits, the
  recommended option first, and a short reason in that option's description.
  Wait for the answers.
- Do not print interview questions, choices, or recommended answers as
  assistant feed text. Chat may give brief context or the complete plan; the
  decisions themselves belong in the question prompt.
- If the runtime has no interactive question prompt, fall back to this chat
  format and wait:

  ```
  ❓ **Q1** - **<title>**: <question and choices>

  ➡️ <recommended answer>
  ```

- A question that depends on an answer still open in this round belongs to a
  later round.
- Record the user's answer, not the recommendation or conversation. Update the
  matching active plan after every round: `docs/plan.md` for a new or updated
  strategy, or `docs/replacement-plan.md` for a staged replacement. Surface
  contradictions immediately. Preserve `contract_version` until the versioning
  workflow authorizes advancing it.
- Use plain trading language for a user who understands profit, loss, fees,
  trades, and percentage limits. Avoid specialist terms when familiar words
  work. If a specialist term is necessary, explain it immediately; for
  example, describe drawdown as the largest drop from a previous high.
- Make each question easy to answer by including a brief example or two or
  three short choices. Use earlier answers to recommend a concrete choice that
  the user can accept or adjust instead of asking them to invent an answer from
  scratch.
- Challenge lookahead, overfitting, unavailable data, timing mismatches,
  hidden cost, unreliable execution, and unnecessary complexity. Offer the
  simplest feasible alternative and resolve the choice.
- Allow conservative defaults for incidental mechanics. Label them as agent
  defaults so the user accepts them with the complete plan.
- Treat API-key permissions, owned-strategy discovery, eligibility, account
  limits, and endpoint fields as discoverable facts. Follow
  `alphainsider-target.md` and `credentials.md` rather than
  asking the user to find IDs, scopes, or account details.
- Do not code while the plan is `draft`. When the tree is complete, present
  one normalized complete plan for confirmation.

## Existing project

After preflight recognizes and checks a project under `versioning.md`, ask
exactly one existing-project question through the interactive question prompt:
"Would you like to update the existing plan, replace the trading strategy with
a new one, or retire and clean it up?" Present those as three short choices and
recommend updating because it preserves prior decisions.

- For **update**, preserve unaffected decisions and interview only the choices
  the requested change affects. Return a `confirmed` or `implemented` plan to
  `draft` before recording the exact action inventory. For an older project,
  complete the combined target audit and exact-path decisions in
  `versioning.md`. Do not ask a behavior question for a documentation-only gap.
- For **replace**, leave the current plan and implementation untouched. Create
  or resume `docs/replacement-plan.md` on the installed version and run the
  complete design tree for the new strategy. Do not upgrade the outgoing
  strategy. Ask the outgoing remote-disposition decision when that frontier is
  unblocked. Inventory every exact replacement action while the replacement is
  draft; final confirmation sets them to `confirmed` and authorizes the exact
  recorded deletion, promotion, cleanup, and implementation actions without
  another approval.
- For **retire**, leave the active plan and implementation unchanged while
  drafting. Follow `cleanup.md`. Retirement always preserves an auditable
  retired plan and asks whether the verified owned AlphaInsider target should
  be retained and detached or deleted.

Resume `docs/replacement-plan.md` when it is a recognized `draft` or
`confirmed` plan. Treat any other existing file at that path as an ordinary
collision. Otherwise create it from `plan-template.md` after the first
interview answer and update it after every round. Do not modify `docs/plan.md`
or any current implementation artifact while drafting.

Before confirmation, inventory attributable source, tests, copied
AlphaInsider helpers, dependencies, `.env.example`, `.gitignore`, `README.md`,
`AGENTS.md`, and every attributable native definition, agent task, and running
state. Show and record every exact deletion, overwrite, promotion, stop, pause,
disable, activation, native-definition, and agent-task action. Never
recursively delete the project root.
Never delete `.env`, credentials, caches, unrelated files, or files whose
ownership is uncertain.

If the user does not confirm, retain the replacement plan as `draft`. If a
valid replacement plan is already `draft`, resume its next unresolved
frontier. If it is `confirmed`, use `implementation.md` to perform only the
recorded actions without another interview or approval.

Resume unfinished remote deletion only when the user explicitly asks to clean
up or continue that cleanup.

## Design tree

1. **Objective** — Ask "What do you want this strategy to do?" and record the
   answer as the strategy goal.
2. **Market and instruments** — Choose the strict `stock` or `cryptocurrency`
   asset class and an instrument-selection mode: `fixed`, `dynamic`, or
   `constrained dynamic`. For fixed selection, record explicitly named
   instruments; validate their mappings later in the AlphaInsider phase. For
   dynamic selection, define the runtime selector without requiring an advance
   list. For constrained dynamic selection, define the category, allowlist, or
   other boundary within which runtime selection may operate. Every traded
   candidate must match the planned asset class.
3. **Strategy behavior** — Define every input, transformation, entry decision,
   exit or holding rule, and tie-breaking behavior. Prefer deterministic rules.
   For an LLM or hosted model, additionally define the prompt/input contract,
   output schema, model expectations, cost ceiling, timeout, invalid-output
   handling, and fallback. Resolve bar or event timing, polling or streaming,
   schedule, market-hours behavior, decision latency, late events, and when an
   order is evaluated relative to its signal.
4. **Data and resources** — After cadence exists, this phase may share a
   frontier with execution and backtesting. Derive technical requirements
   before selecting tools. Research current primary documentation for plausible
   sources and libraries; check coverage, history, timestamps, latency,
   authentication, price, rate limits, licensing, reliability, and maintenance
   burden. Recommend the smallest stack and record routine selections as agent
   defaults. Ask the user only when cost, credentials, scraping, or another
   meaningful tradeoff needs their decision. Resolve required inputs, as-of
   timing, freshness, and missing, stale, delayed, or conflicting data
   behavior. Prefer AlphaInsider's applicable stock REST endpoints and
   `wsStockPrice` for supported current instrument metadata, exchange status,
   and bid, ask, or last prices when their coverage, freshness, and cadence fit.
   Use an external provider when AlphaInsider does not supply the required live
   market, cadence, freshness, or signal-specific input. For historical inputs
   used by live operation, compare AlphaInsider and external sources case by
   case under the same research criteria. Offer scraping only with permitted
   access, no suitable supported feed, a documented failure/maintenance plan,
   and a recorded user decision before final confirmation.
5. **Execution and risk** — Resolve fixed versus allocation orders, types,
   sizing, entries, reductions, exits, and position/open-order reconciliation;
   apply the sibling AlphaInsider skill's normalized sizing/order rules. For
   allocations or webhook leverage, ask a separate maximum-exposure question:
   100% is 1× portfolio value, while AlphaInsider permits up to 200% (2×).
   Treat 200% as the platform ceiling, not a default; do not assume 100% is the
   platform maximum. Record the user's chosen cap under sizing and exposure
   constraints. Buying power, fees, and slippage may lower executable exposure.
   Use `getMaxOrderSize` as the fixed-order authority. Resolve
   position/exposure limits, stops or exit constraints, in-process retries,
   duplicate events, automatic pause or shutdown conditions, logging, and
   recovery. For dynamic instruments, resolve validation freshness and whether
   one invalid candidate causes the cycle to continue with valid candidates or
   abort. Propose safe, simple defaults when the strategy does not require a
   special choice.
6. **Backtesting** — Determine whether every signal input and decision timestamp
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
7. **Implementation** — Resolve language when Python is unsuitable, module
   responsibilities, data flow, persistent state, configuration names, the
   finite one-cycle command, persistent command when applicable, tests to run,
   and expected results.
   Select routine implementation details as agent defaults; ask the user only
   when a material tradeoff requires their decision. Require the generated
   README's short startup sequence to use those exact language-specific setup
   and run commands; for Python, include `source .venv/bin/activate` before the
   run choices. Do not add an interactive confirmation to an operational
   command. A user-run command is the user's execution action. Never manually
   run a cycle, start a persistent process, or trigger a schedule during build
   and verification.
   Treat the selected project root as `.` in every persisted project path;
   never embed machine-specific absolute paths except in confirmed native
   operation definitions, or write generated artifacts into an installed skill
   directory.
8. **Operation and scheduling** — After cadence, worst-case cycle duration, and
   host discovery, follow `operation-and-scheduling.md`. Distinguish a single
   run, persistent process, and recurring schedule. Foreground supports a
   single run or visible persistent process. Native user-system operation may
   use a Linux systemd or macOS launchd persistent service, or recurring finite
   cycles through systemd timers, launchd calendar intervals, or Windows Task
   Scheduler. An available agent scheduler may run a recurring standalone task
   locally or in an already prepared remote or web runtime; each occurrence
   runs exactly one finite cycle. Resolve capability, collision, schedule,
   missed-run, non-overlap, retry, activation, log or history, notification,
   and installation decisions without creating or starting a resource.
   Recommend active for a first-session ready target.
9. **AlphaInsider target** — After class and execution, follow
   `alphainsider-target.md`. Resolve a compatible target and instrument
   validation when possible; otherwise record explicit local-only readiness.
   Verify that the target's owner context and multiplier do not invalidate
   planned sizing or risk behavior. Reopen only affected earlier decisions when
   they do, rerun every dependent phase, and return here before confirmation.

Objective unblocks market. Market unblocks behavior. Behavior cadence unblocks
data, execution, and backtesting as one frontier. Implementation defaults may
join that frontier when no material language tradeoff exists. Operation waits
for cadence, worst-case duration, and host facts. Target waits for class and
execution. Confirmation waits for a complete tree.

## Missing environment values

A missing API key or other required credential is a setup gap, not a strategy
decision. Follow `credentials.md`. Name the missing variables
and exact project `.env` path, then recommend that the user add the values there
themselves and tell you when ready. If the user wants agent-assisted entry,
they may paste values in chat so you can add them. Always warn first that
pasting credentials is less secure because each value is visible to the agent
and may appear in tool metadata or a transient process listing.
A missing `ALPHAINSIDER_STRATEGY_ID` follows the target branch above instead of
being treated as a credential gap.

During AlphaInsider forward-test setup, an unavailable or insufficient
`ALPHAINSIDER_API_KEY` permits explicit local-only target readiness and
continuation to plan confirmation; it never permits a remote call. A missing
credential required to validate another selected data source pauses that
affected branch until the user supplies it or selects a feasible alternative.

For pasted values, follow `credentials.md`. Use the sibling request helper for
AlphaInsider strategy configuration only when the target is not local-only.

## Confirmation gate

Complete plan confirmation is the only skill-level execution approval. Before
presenting the plan:

- Require target readiness to be exactly `ready` or `local-only`. For `ready`,
  verify the permission bundle, compatible ownership and type, complete core
  creation fields, and explicit mappings or runtime validation contract. For
  `local-only`, record a non-secret reason and normalize target-dependent
  fields; do not leave `_pending_` or `_not yet decided_` placeholders.
- Ensure the selected data and library stack is available and resolve every
  cost, credential, scraping, or other material tradeoff as a recorded
  interview decision.
- Require operation and scheduling to contain one compatible invocation model
  and runner with every applicable dependent decision complete. Include every
  exact native definition or agent task, active or inactive state, future-login
  effect or next scheduled run, missed-run acceptance, and runtime-location
  requirement in the complete plan.
- Ensure no unresolved placeholder or contradiction remains outside the
  explicitly local-only target fields.
- Include every exact create, modify, overwrite, delete, stop, pause, disable,
  activation, promotion, provisioning, synchronization, ID-persistence,
  native-operation, and agent-task action. Research collisions and present
  warnings while the plan is draft.
- Include the exact generated AlphaInsider description. Plan confirmation
  authorizes its initial creation value and later synchronization only when
  target readiness is `ready`. For a ready new target, the same confirmation
  is the sole authorization for `newStrategy` and persist its returned
  ID on this plan; do not request another creation confirmation.
- For an upgrade, ensure the installed target contract and its applicable tests
  conform before advancing `contract_version`; never advance to a remote
  version that this installed skill does not contain.
- State backtesting as unavailable, declined, or accepted with its exact scope.
- Present the complete normalized plan, including every agent default and
  exact action, and ask once for final confirmation through the interactive
  question prompt, not as ordinary chat text. That confirmation is the
  only skill-level execution approval; do not request another approval for any
  confirmed implementation or update action. Never request a one-off approval
  against a confirmed plan.
- Confirmation with a `local-only` target authorizes a complete local build,
  including AlphaInsider adapters, order mapping, documentation, backtests, and
  mocked tests, but no remote calls or order-submitting commands. Keep the plan
  `confirmed`, never `implemented`, and mark operational commands unavailable
  until target readiness is resolved. Retain operation decisions but create no
  native definition or agent task.
- To resume a local-only target, return the plan to `draft`, preserve every
  unaffected decision, interview only target gaps, and reconfirm the complete
  plan before provisioning, synchronization, or any other remote work.
- For a replacement, include the exact deletion list, stop/disable effects,
  target disposition, live-state warning, overwrites, and promotion in the
  replacement draft. Final replacement-plan confirmation authorizes all of
  them; do not use a separate deletion, cleanup, or promotion gate. A
  local-only replacement target authorizes none of the outgoing cleanup
  actions.
- For retirement, require the plan's exact target ID and ownership, operation
  shutdown, local path inventory, preserve list, remote disposition, binding
  action, and ordered failures. Its one final confirmation is the sole
  cleanup execution approval.
- If any required action, identity, or path was absent or changes afterward,
  return the plan to `draft`, resolve only the affected decisions, and present
  the complete plan for one new final confirmation.
