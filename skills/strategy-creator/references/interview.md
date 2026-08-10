# Strategy Interview

Use this decision tree adaptively. Resolve dependencies before downstream
questions and skip branches that cannot affect the project.

## Contents

- [Protocol](#protocol)
- [Existing project branch](#existing-project-branch)
- [AlphaInsider forward-test setup branch](#alphainsider-forward-test-setup-branch)
- [Decision tree](#decision-tree)
- [Missing environment values](#missing-environment-values)
- [Confirmation gate](#confirmation-gate)

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
  `alphainsider-target.md` and `credentials.md` rather than
  asking the user to find IDs, scopes, or account details.

## Existing project branch

After preflight recognizes and checks a project under `versioning.md`, ask
exactly one question:
"Would you like to update the existing plan or replace the trading strategy
with a new one?" Present those as two short choices and recommend updating
because it preserves prior decisions.

- For **update**, preserve unaffected decisions and interview only the choices
  the requested change affects. Return a `confirmed` or `implemented` plan to
  `draft` before recording the exact action inventory. For an older project,
  complete the combined target audit and exact-path decisions in
  `versioning.md`. Do not ask a behavior question for a documentation-only gap.
- For **replace**, leave the current plan and implementation untouched. Create
  or resume `docs/replacement-plan.md` on the installed version and run the
  complete decision tree for the new strategy. Do not upgrade the outgoing
  strategy. Inventory every exact replacement action while the plan is draft;
  final confirmation sets it to `confirmed` and authorizes the exact recorded
  deletion, promotion, and implementation actions without another approval.

Resume `docs/replacement-plan.md` when it is a recognized `draft` or
`confirmed` plan. Treat any other existing file at that path as an ordinary
collision. Otherwise create it from `plan-template.md` after the first
interview answer and update it after every answer. Do not modify `docs/plan.md`
or any current implementation artifact while drafting.

Before confirmation, inventory attributable source, tests, copied
AlphaInsider helpers, dependencies, `.env.example`, `.gitignore`, `README.md`,
`AGENTS.md`, and any attributable background definition and running state.
Show and record every exact deletion, overwrite, promotion, stop, disable, and
background-definition action. Never recursively delete the project root.
Never delete `.env`, credentials, caches, unrelated files, or files whose
ownership is uncertain.

If the user does not confirm, retain the replacement plan as `draft`. If a
valid replacement plan is already `draft`, resume its next unresolved
decision. If it is `confirmed`, use `implementation.md` to perform only the
recorded actions without another interview or approval.

## AlphaInsider forward-test setup branch

Enter this branch after the strategy's market, behavior, execution, risk,
resource, and background-operation decisions and before backtesting. Follow
`alphainsider-target.md`:

- Run the API-key permission gate, then validate a configured target or
  discover owned strategies. Require the target to match the already planned
  strict asset class and execution requirements.
- If the configured target is incompatible, preserve the strategy and offer a
  compatible owned target or a new target. Also allow the user to reopen the
  affected market or strategy decisions instead. Never silently change either
  the strategy or its configured target.
- Ask the user to select an owned compatible strategy or explicitly choose a
  new strategy; never choose the first result or create a duplicate silently.
  Persist the user's selection through the non-echoing helper and record
  `selected existing` without its ID.
- For a new target, use the planned asset class, propose a short name from the
  goal, require the owner starting balance, and offer only access modes allowed
  by the verified account checks. Present the exact core fields and obtain
  each required decision while the plan is draft. Do not ask for separate
  creation approval; also resolve failed-current-run retain-or-delete behavior.
  Complete plan confirmation covers the recorded fields and cleanup policy.
- Validate mappings for explicitly named instruments. For dynamic selection,
  confirm that runtime lookup, asset-class checks, freshness, and invalid-
  candidate behavior are complete.
- Draft the exact remote description from the completed strategy decisions.
  Do not call `newStrategy` while the plan is draft.
- Record target readiness as `ready` only after the applicable permission,
  compatibility, validation, and creation-field decisions are complete. If
  setup is blocked, record `deferred` with a non-secret reason, normalize every
  unavailable target field as deferred rather than leaving a placeholder, make
  no further remote calls, and continue to backtesting.

## Decision tree

1. **Intent** — Ask "What do you want this strategy to do?" and record the
   answer as the strategy goal.
2. **Market and instruments** — Choose the strict `stock` or `cryptocurrency`
   asset class and an instrument-selection mode:
   `fixed`, `dynamic`, or `constrained dynamic`. For fixed selection, record
   explicitly named instruments; validate their mappings later in the
   AlphaInsider phase. For dynamic selection, define the runtime selector
   without requiring an advance list. For constrained dynamic selection,
   define the category, allowlist, or other boundary within which runtime
   selection may operate. Every traded candidate must match the planned asset
   class.
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
   constraints, missing/stale data behavior, in-process retries, duplicate
   events, automatic pause or shutdown conditions, logging, and recovery. For
   dynamic instruments, resolve validation freshness and whether
   one invalid candidate causes the cycle to continue with valid candidates or
   abort. Propose safe, simple defaults when the strategy does not require a
   special choice.
7. **Resources** — Derive technical requirements before selecting tools.
   Research current primary documentation for plausible sources and libraries;
   check coverage, history, timestamps, latency, authentication, price, rate
   limits, licensing, reliability, and maintenance burden. Recommend the
   smallest stack and record routine selections as agent defaults. Ask the user
   only when cost, credentials, scraping, or another meaningful tradeoff needs
   their decision. Prefer AlphaInsider's applicable stock REST endpoints and
   `wsStockPrice` for supported current instrument metadata, exchange status,
   and bid, ask, or last prices when their coverage, freshness, and cadence fit.
   Use an external provider when AlphaInsider does not supply the required live
   market, cadence, freshness, or signal-specific input. For historical inputs
   used by live operation, compare AlphaInsider and external sources case by
   case under the same research criteria. Offer scraping only with permitted
   access, no suitable supported feed, a documented failure/maintenance plan,
   and a recorded user decision before final confirmation.
8. **Background operation** — Read and follow
   `background-operation.md`. Always ask whether the continuous strategy should
   run in the background. If declined, record foreground-only operation and
   skip dependent questions. If accepted, discover usable user-level managers,
   then resolve the selected manager and identifier, login autostart when
   supported, failure restart behavior, bounded systemd retry parameters when
   selected, log exposure and retention, collision state, and installation
   readiness. Resolve missing manager support before confirmation. Never offer
   background execution for the one-cycle command.
9. **AlphaInsider forward-test setup** — Run the branch above. Resolve a
   compatible target and instrument validation when possible; otherwise record
   explicit deferral. Verify that the target's owner context and multiplier do
   not invalidate planned sizing or risk behavior. Reopen only affected
   strategy decisions when they do, then rerun their downstream branches.
10. **Backtesting** — Determine whether every signal input and decision timestamp
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
11. **Implementation contract** — Resolve language when Python is unsuitable,
   module responsibilities, data flow, persistent state, configuration names,
   one-cycle and continuous commands, tests to run, and expected results.
   Select routine implementation details as agent defaults; ask the user only
   when a material tradeoff requires their decision.
   Require the generated README's short startup sequence to use those exact
   language-specific setup and run commands; for Python, include
   `source .venv/bin/activate` before the run choices.
   Do not add an interactive confirmation to the one-cycle or continuous
   command. Running either command is the user's execution action. Never start
   either command automatically or during build and verification.
   Treat the selected project root as `.` in every persisted project path;
   never embed machine-specific absolute paths except in the confirmed native
   host definition, or write generated artifacts into an installed skill
   directory.

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
`ALPHAINSIDER_API_KEY` permits explicit target deferral and continuation to
backtesting; it never permits a remote call. A missing credential required to
validate another selected data source pauses that affected branch until the
user supplies it or selects a feasible alternative.

For pasted values, follow `credentials.md`: run the agent-only
`scripts/set_env_value.py NAME VALUE` command from the project root once per
variable and pass the value as exactly one safely quoted argument. Never show
the command to the user, import or call the helper, reproduce its logic, use
inline Python, a shell pipeline, environment variable, temporary file, patch,
or direct `.env` edit, open `.env`, repeat a value, or put one in a plan. If the
runtime cannot pass one safely quoted argument, return to the documented
user-edit workflow. Use the sibling request helper for AlphaInsider strategy
configuration only when the target is not deferred.

## Confirmation gate

Before presenting the plan for confirmation:

- Require target readiness to be exactly `ready` or `deferred`. For `ready`,
  verify the permission bundle, compatible ownership and type, complete core
  creation fields, and explicit mappings or runtime validation contract. For
  `deferred`, record a non-secret reason and normalize target-dependent fields;
  do not leave `_pending_` or `_not yet decided_` placeholders.
- Ensure the selected data and library stack is available and resolve every
  cost, credential, scraping, or other material tradeoff as a recorded
  interview decision.
- Require background operation to be normalized as foreground-only or as one
  usable selected manager with every applicable dependent decision complete.
  Include the exact inactive host definition path and any future-login
  autostart effect in the complete plan.
- Ensure no unresolved placeholder or contradiction remains outside the
  explicitly deferred target fields.
- Include every exact create, modify, overwrite, delete, stop, disable,
  promotion, provisioning, synchronization, ID-persistence, and host-install
  action. Research collisions and present warnings while the plan is draft.
- Include the exact generated AlphaInsider description. Plan confirmation
  authorizes its initial creation value and later synchronization only when
  target readiness is `ready`. For a ready new target, the same confirmation
  is the sole authorization for `newStrategy` and persistence of its returned
  ID; do not request another creation confirmation.
- For an upgrade, ensure the installed target contract and its applicable tests
  conform before advancing `contract_version`; never advance to a remote
  version that this installed skill does not contain.
- State backtesting as unavailable, declined, or accepted with its exact scope.
- Present the complete normalized plan, including every agent default and
  exact action, and ask once for final confirmation. That confirmation is the
  only skill-level execution approval; do not request another approval for any
  confirmed implementation or update action.
- Confirmation with a `deferred` target authorizes a complete local build,
  including AlphaInsider adapters, order mapping, documentation, backtests, and
  mocked tests, but no remote calls or order-submitting commands. Keep the plan
  `confirmed`, never `implemented`, and mark operational commands unavailable
  until target readiness is resolved. Retain background decisions but install
  no host definition.
- To resume a deferred target, return the plan to `draft`, preserve every
  unaffected decision, interview only target gaps, and reconfirm the complete
  plan before provisioning, synchronization, or any other remote work.
- For a replacement, include the exact deletion list, stop/disable effects,
  overwrites, and promotion in the draft. Final replacement-plan confirmation
  authorizes all of them; do not use a separate deletion or promotion gate.
- If any required action or path is discovered or changes after confirmation,
  return the plan to `draft`, resolve only the affected decisions, and present
  the complete plan for one new final confirmation. Never request a one-off
  approval against a confirmed plan.
