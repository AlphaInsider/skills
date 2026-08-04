---
name: strategy-creator
description: Interview users one decision at a time, maintain a decision-complete plan, and build, test, backtest, document, or change one automated AlphaInsider paper-trading strategy. Use for stock or cryptocurrency strategies that may depend on market data, models, APIs, or authorized web data but send orders only to AlphaInsider.
---

# AlphaInsider Strategy Creator

Use this skill as an instruction manual with one local `.env` setup helper.
Build only the project justified by the confirmed strategy plan; this skill
contains no provider or runtime code.

## Scope

- Build one fully automated AlphaInsider paper-trading strategy per project.
- Fix the project to the configured AlphaInsider strategy's explicit asset
  class: `stock` or `cryptocurrency`. Every traded instrument must match that
  class. Cross-asset and alternative data may inform signals but cannot expand
  it.
- Support fixed, dynamic, and constrained-dynamic instrument selection. Do not
  require a predefined instrument list when the strategy selects candidates at
  runtime.
- Use AlphaInsider as the only order destination. Never instantiate a live
  broker trading client.
- Map the project to the user's AlphaInsider strategy through
  `ALPHAINSIDER_STRATEGY_ID` in `.env`.
- Never inspect or print existing `.env` values or API keys. When a required
  value is missing, offer the user the credential setup choices below.
- Treat this skill directory and the sibling `alphainsider` skill directory as
  read-only sources. The setup helper may be executed from the selected project
  root, but never create, edit, format, or delete files in either skill.
- Write every generated strategy artifact inside the selected project root.

## Preflight

1. Locate this skill and the sibling `alphainsider` skill. Require this skill's
   `scripts/set_env_value.py` plus the sibling's `SKILL.md`,
   `scripts/alphainsider_request.py`, and `scripts/runtime/` before doing any
   work. If missing, stop and ask the user to install both skills:

   ```bash
   npx skills@latest add https://github.com/AlphaInsider/skills \
     --skill alphainsider --skill strategy-creator
   ```

2. Read [references/interview.md](references/interview.md) and
   [references/plan-template.md](references/plan-template.md) in full.
3. Ask for the project root, recommending the directory from which the user
   invoked the skill. Accept a normal user-controlled project location,
   including a suitable project directory beneath the user's home, when the
   required files can be added safely. Reject an installed skill directory, an
   obviously unsafe system location, or a location where the project cannot be
   created. Use reasonable judgment; do not maintain an exhaustive path
   denylist or perform elaborate filesystem checks. If unsuitable, explain why
   and ask for another path.
4. Inspect `docs/plan.md` without opening `.env`. Recognize the root as a
   project created by this skill only when that file has a valid `draft`,
   `confirmed`, or `implemented` status, the `# Strategy Plan` title, and every
   section heading from the current plan template. Do not require the current
   field wording; this stable signature covers earlier projects that use the
   same plan lifecycle and sections.
5. For a recognized project, ask exactly one question before any strategy
   interview: whether to **update the existing plan** or **replace the trading
   strategy with a new one**. Recommend updating because it preserves prior
   decisions.
   - For an update, preserve unaffected decisions, keep a `draft` plan in that
     state, and return a `confirmed` or `implemented` plan to `draft` before
     changing behavior. Interview only the affected decisions.
   - For a replacement, follow the replacement lifecycle below. Do not alter
     the current plan or implementation while interviewing the replacement.
6. Inspect the rest of the selected project root without opening `.env`; list
   only files this workflow would create or change that already exist. Treat
   collisions other than recognized plan files as ordinary file conflicts and
   obtain explicit overwrite approval. Preserve unrelated files.

Do not recognize or migrate legacy manifests, checkpoints, backups, generated
runtime layouts, provider modules, or plan schemas. Do not create replacement
backups or management metadata.

## Environment setup

When validation or a generated strategy reports a missing required environment
variable:

1. Name the missing variable or variables and show the exact selected-project
   `.env` path without opening that file.
2. Ask the user to either add the values to `.env` and tell you when ready, or
   paste them in chat so you can add them. Warn that pasting credentials in
   chat is less secure. For one missing variable, accept a bare value; for
   several, request one `NAME=value` line per variable.
3. Treat pasted values as approval to update only those names in `.env`. Never
   echo, quote, summarize, log, or record them in plans, `.env.example`, source,
   tests, documentation, or command arguments.
4. For each pasted value, run the following from the selected project root and
   supply the value only through the helper's non-echoing prompt:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/set_env_value.py NAME
   ```

   Do not open `.env` before or after the update. The helper preserves unrelated
   entries and writes only the requested name. Pasted-value approval is also
   approval for that exact `.env` update; do not ask a separate collision
   question.
5. Rerun the non-ordering validation that reported the missing value. For
   AlphaInsider configuration, use the sibling request helper and report only
   the validation result, never credentials or strategy IDs.

## Plan lifecycle

Use `docs/plan.md` as the source of truth for the current strategy. During a
replacement, use `docs/replacement-plan.md` as the prospective plan while the
current plan remains authoritative. Both plans use only `draft`, `confirmed`,
and `implemented`.

### Replacement

1. When the user chooses replacement, resume `docs/replacement-plan.md` if it
   has the current plan signature and is `draft` or `confirmed`. Treat any
   other existing file at that path as an ordinary collision and obtain
   explicit overwrite approval before starting a new replacement plan.
2. For a new replacement, create `docs/replacement-plan.md` from the plan
   template on the first confirmed interview answer. Follow the complete
   interview from intent onward and update that file after every answer. Do not
   modify `docs/plan.md` or any current implementation artifact.
3. Explicit confirmation changes the replacement plan to `confirmed`, but does
   not authorize deletion, plan promotion, or implementation. Inventory the
   exact old artifacts attributable to this skill, using the current plan and
   project contents. Include generated strategy source, tests, copied runtime,
   dependency configuration, `.env.example`, `.gitignore`, `README.md`, and
   `AGENTS.md` when present and attributable to the current strategy.
4. Show the exact proposed deletion paths and ask for separate explicit
   approval that also covers replacing `docs/plan.md` with the confirmed
   replacement plan. Never recursively delete the project root. Never delete
   `.env`, credentials, caches, unrelated files, or files whose ownership is
   uncertain.
5. If the user declines, leave the current plan and implementation unchanged
   and retain the confirmed replacement plan for later resumption.
6. If the user approves, delete only the approved paths, replace
   `docs/plan.md` with `docs/replacement-plan.md`, remove the temporary path,
   and follow the Confirmed workflow to build the replacement. After complete
   offline verification, set the promoted plan to `implemented`.

Plan confirmation and deletion approval are separate decisions. Never delete
or reimplement the current strategy based only on replacement-plan
confirmation.

### Draft

1. On the first confirmed interview answer, create `docs/plan.md` from the
   plan template after obtaining permission to create or replace that path.
2. Follow the interview reference. Ask exactly one decision question per turn,
   recommend an answer with a short reason, wait for the response, and write
   the normalized answer immediately. Do not preserve the transcript.
3. Research discoverable facts instead of asking the user. When requirements
   are known, research current data sources and libraries using primary
   documentation. Recommend the smallest feasible stack and obtain the user's
   confirmation before recording it.
4. Prefer Alpaca for equities and Coinbase for cryptocurrency when they meet
   the requirements. Treat scraping as an explicitly approved, authorized
   fallback when a supported API or feed is unsuitable.
5. Prefer deterministic signal logic. Permit hosted models only when the plan
   defines their inputs, outputs, version expectations, cost limits, timeouts,
   failure behavior, and replay limitations.
6. Before confirmation, use the sibling skill's request helper for read-only
   validation of the configured AlphaInsider strategy and its asset class. If
   the user explicitly names instruments, also validate their AlphaInsider
   mappings. For dynamic selection, record the runtime resolution contract
   without requiring candidate mappings in advance. Let the helper read
   `.env`; never read it yourself. If configuration is missing, follow
   **Environment setup** above. Record validation results without credentials
   or strategy IDs.
7. Offer backtesting only when every decision input can be reconstructed as it
   was known at the decision time. If feasible, ask whether the user wants it;
   if accepted, resolve the window and scope. Otherwise record why it would be
   misleading or infeasible.
8. Resolve contradictions and implementation-blocking decisions, then present
   the complete normalized plan. Explicit confirmation of `docs/plan.md`
   changes the status to `confirmed` and authorizes implementation immediately.
   Confirmation of `docs/replacement-plan.md` stops at the separate deletion
   gate above.

Do not generate strategy code while the plan is `draft`. Conservative agent
defaults are allowed for incidental mechanics only when labeled in the plan;
the final confirmation must make them visible and accepted.

### Confirmed

Read the relevant sibling AlphaInsider references before writing integration
code, especially authentication, runtime-client, stocks, trades,
input-multiplier, and WebSocket guidance as applicable.

Before writing, inventory every exact project path the confirmed plan will
create or change. Plan confirmation authorizes new files, but an existing file
still requires explicit overwrite approval. Keep every write inside the
selected project root. Use machine-specific absolute paths only to locate the
project during the current run; persist project-relative paths in the project.

Build the smallest standalone project that satisfies the plan:

- Use Python by default. Use another language only when the plan records a
  concrete ecosystem reason and an equivalent AlphaInsider integration.
- Create `strategy/`, `tests/`, `.env.example`, ecosystem dependency
  configuration, `.gitignore`, `README.md`, and `AGENTS.md`. Keep internal
  modules specific to the strategy instead of imposing a generic framework.
- For Python, read the sibling `scripts/runtime/client.py` as an immutable
  source and copy it into the project; copy `stream.py` only when WebSockets are
  required. Preserve credential and normalized-value behavior and adjust the
  project copies without modifying or duplicating clients in either skill.
- Put only variable names and safe examples in `.env.example`. Keep `.env`,
  credentials, caches, and build artifacts ignored; keep the plan, source,
  tests, and documentation commit-ready. Use **Environment setup** for any
  required value that is still missing.
- Expose project-native commands for one decision cycle, continuous operation,
  tests, and an optional backtest when selected. Do not add a dry-run mode.
- Implement the plan's `fixed`, `dynamic`, or `constrained dynamic` instrument
  selection mode. For each actionable runtime candidate that lacks an exact
  AlphaInsider ID, use `search_stocks` and reject missing or ambiguous matches;
  never guess a mapping. Validate resolved IDs with `get_stocks`, batching
  candidates when practical, and require each returned `security` to equal the
  configured strategy's `stock` or `cryptocurrency` type before ordering.
- Never submit an order for an unvalidated, missing, ambiguous, or mismatched
  instrument. Revalidate newly selected or changed candidates according to the
  plan's freshness rule. On validation failure, follow the plan-specific choice
  to continue with valid candidates or abort that decision cycle.
- Reconcile relevant AlphaInsider positions and open orders before decisions,
  validate the configured strategy type at startup, and implement the plan's
  stale-data, retry, duplicate-event, recovery, logging, sizing, and risk
  behavior. Never treat a missing `input_multiplier` as `1`.
- Keep decision logic independently testable. When backtesting is selected,
  replay production decisions chronologically without AlphaInsider calls or
  future information. For dynamic selection, reconstruct the historical
  candidate set as it existed at each decision time without survivorship bias.
  Add portfolio accounting only when its execution and cost assumptions are
  credible and documented.

After implementation, create strategy-specific offline tests for signals,
risk rules, order mapping, orchestration, and backtesting when selected. Mock
all external services. Tests and implementation verification must never submit
AlphaInsider orders; do not run an order-submitting command merely to verify
the build.

Write `README.md` for humans: purpose, behavior, prerequisites, setup,
environment variable names, commands, monitoring, limitations, and recovery.
Include a short `## Start` section with ordered, copy-paste commands for
dependency installation and `.env` preparation. Label the exact commands for
one decision cycle and continuous operation equally. Match the selected
language and keep explanations brief. For Python, place
`source .venv/bin/activate` immediately before the execution commands. For any
other language, use the project's exact package-manager and runtime commands;
do not include Python steps.
Write `AGENTS.md` for agents: treat `docs/plan.md` as authoritative, preserve
the credential boundary and missing-variable setup choices, identify code/test
entry points, and require the maintenance workflow below.

Run the complete offline suite and static checks. When code, tests, plan, and
documentation agree, set the plan status to `implemented`. Deployment or
hosting is outside this workflow unless the user separately requests it.
Before handoff, confirm that every created or changed strategy path belongs to
the selected project root and that no operation wrote to either skill
directory.

### Implemented

For any behavior change, return the plan to `draft`, interview the affected
decisions one at a time, and obtain confirmation before editing code. Then
update implementation, tests, `README.md`, and `AGENTS.md` together and restore
`implemented` only after verification passes.
