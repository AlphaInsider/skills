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
- Use AlphaInsider as the only order destination; never create a live-broker
  client. Select its strategy through `ALPHAINSIDER_STRATEGY_ID` in `.env`.
- Keep the configured `stock` or `cryptocurrency` asset class. Signals may use
  cross-asset or alternative data, but every traded instrument must match.
- Support fixed, dynamic, and constrained-dynamic selection without requiring
  a predefined runtime candidate list.
- Never inspect or print existing `.env` values or API keys. Use the credential
  workflow below when values are missing.
- Treat this skill directory and the sibling `alphainsider` skill directory as
  read-only sources. Run the setup helper only from the selected project root;
  write all generated artifacts there and never modify either skill.

## Preflight

1. Require this skill's `scripts/check_for_update.py` and
   `scripts/set_env_value.py`, plus the sibling `alphainsider` skill's
   `SKILL.md`, `scripts/alphainsider_request.py`, and
   `scripts/alphainsider_stream.py`. If missing, stop and request both skills:

   ```bash
   npx skills@latest add https://github.com/AlphaInsider/skills \
     --skill alphainsider --skill strategy-creator
   ```

2. Run the advisory repository check once per invocation before other work:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/check_for_update.py
   ```

   If it prints a notice, show it once but never run or offer to run its update
   command. Continue with this installed skill. If it prints nothing or the
   check cannot run, continue silently.
3. Read [references/interview.md](references/interview.md),
   [references/plan-template.md](references/plan-template.md), and
   [references/versioning.md](references/versioning.md) in full.
4. Ask for the project root; recommend the invocation directory. Accept a
   normal user-controlled project location, including a suitable project
   directory beneath the user's home, when writable. Reject an installed skill
   directory, an obviously unsafe system location, or an unusable location.
   Use judgment; do not maintain an exhaustive path denylist or perform
   elaborate filesystem checks. Explain rejections and ask for another path.
5. Without opening `.env`, recognize and compare existing projects exactly as
   specified in `references/versioning.md`. A valid version marker takes
   precedence; only an unversioned plan with the complete current signature is
   legacy `0.0.0`. Stop on malformed or newer project versions. Compare only
   with the installed version, never the repository version reported by the
   advisory check.
6. For a recognized project, ask exactly one question before the interview:
   whether to **update the existing plan** or **replace the trading strategy
   with a new one**. Recommend updating. For an update, preserve unaffected
   decisions, keep `draft` as-is, return later states to `draft`, and interview
   only affected decisions. If its version is older, follow the direct target
   audit and approval gate in `references/versioning.md` first. For replacement,
   start on the installed version and follow that lifecycle without upgrading
   or altering the current plan or implementation.
7. Without opening `.env`, list only existing paths this workflow would change.
   Treat other collisions as ordinary conflicts, obtain explicit overwrite
   approval, and preserve unrelated files.

Do not create replacement backups or management metadata.

## Environment setup

For each missing required variable:

1. Name it and show the selected project's exact `.env` path without opening
   the file.
2. Recommend that the user add the values to `.env` themselves and tell you
   when ready.
3. If the user wants agent-assisted entry instead, they may paste the values in
   chat. Warn first that pasting credentials is less secure because the value
   is visible to the agent. Accept a bare value for one variable or one
   `NAME=value` line per variable for several.
4. Pasted values grant approval to update only those names. Never echo, quote,
   summarize, log, or record values in plans, `.env.example`, source, tests,
   documentation, or command arguments.
5. From the project root, pass each value only through this non-echoing prompt:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/set_env_value.py NAME
   ```

   Never pass a credential in a command argument. Do not open `.env` before or
   after the update. The helper preserves other entries. Pasting grants
   approval to update only those names, so do not ask again.
6. Rerun the non-ordering check. For AlphaInsider configuration, use the sibling
   request helper and report only the result, never credentials. Strategy IDs
   and other non-secret values may be reported when the user supplied them or
   explicitly asks for them.

## Plan lifecycle

`docs/plan.md` is authoritative. Stage replacements in
`docs/replacement-plan.md` while the current plan remains active. Both use only
`draft`, `confirmed`, and `implemented` and preserve their `contract_version`
until the versioning workflow authorizes advancing it.

### Replacement

1. When replacing, resume `docs/replacement-plan.md` if versioning recognizes
   it as a strategy plan and it is `draft` or `confirmed`. Apply the installed
   version to a new replacement plan. Treat any other existing file at that
   path as an ordinary collision and obtain overwrite approval.
2. Otherwise create it from the template after the first confirmed answer,
   complete the full interview, and update it after every answer. Do not modify
   `docs/plan.md` or any current implementation artifact.
3. Confirmation sets the replacement to `confirmed` but does not authorize
   deletion, plan promotion, or implementation. Inventory attributable source,
   tests, copied AlphaInsider helpers, dependencies, `.env.example`,
   `.gitignore`, `README.md`, and `AGENTS.md` from the current plan and project.
4. Show the exact proposed deletion paths and request separate explicit
   approval to delete them and replace `docs/plan.md` with the confirmed plan.
   Never recursively delete the project root. Never delete `.env`, credentials,
   caches, unrelated files, or files whose ownership is uncertain.
5. If the user declines, change nothing and retain the confirmed replacement
   plan for later resumption.
6. If approved, delete only the approved paths, replace `docs/plan.md` with
   `docs/replacement-plan.md`, remove the temporary path, build through the
   Confirmed workflow, verify offline, and set the promoted plan to
   `implemented`.

Plan confirmation and deletion approval are separate decisions. Never delete
or reimplement from replacement confirmation alone.

### Draft

1. After permission, create `docs/plan.md` from the template on the first
   confirmed answer.
2. Follow the interview reference: ask one decision per turn, record each
   normalized answer immediately, research discoverable facts and the smallest
   feasible stack, and obtain required confirmations. Do not keep a transcript.
3. Before confirmation, let the sibling request helper read `.env` and validate
   the AlphaInsider strategy and asset class. Validate explicit instrument
   mappings; for dynamic selection, record runtime resolution instead. Follow
   **Environment setup** when needed, and record no credentials or strategy IDs.
4. Resolve contradictions and placeholders, then present the complete plan.
   Explicit confirmation of `docs/plan.md` sets `confirmed` and authorizes
   implementation immediately. Replacement confirmation stops at its deletion
   gate.

Do not code while the plan is `draft`. Label incidental conservative defaults
for acceptance with the complete plan.

### Confirmed

Read the sibling `alphainsider` skill for helper usage and the applicable API
references for authentication, stocks, trades, input-multiplier, and
WebSockets. Inventory every path before writing. Confirmation authorizes new
files, but an existing file still requires explicit overwrite approval. Keep
every write inside the selected project root; use absolute paths only during
the run and persist project-relative paths in the project.

Build the smallest standalone project that satisfies the plan:

- Default to Python; use another language only for a recorded ecosystem reason
  with equivalent AlphaInsider integration. Create `strategy/`, `tests/`,
  `.env.example`, dependency configuration, `.gitignore`, `README.md`, and
  `AGENTS.md` without a generic framework.
- For Python, read the sibling `scripts/alphainsider_request.py` as an immutable
  source and copy it to `strategy/alphainsider_request.py`. Copy
  `scripts/alphainsider_stream.py` to `strategy/alphainsider_stream.py` only
  when the confirmed plan uses WebSockets. Import the generic request and
  calculation helpers, and add project-local endpoint functions only for the
  strategy's actual needs. Preserve credential and normalized-value behavior;
  modify only project copies.
- Put only names and safe examples in `.env.example`. Ignore `.env`, secrets,
  caches, and build outputs; keep plans, source, tests, and docs commit-ready.
  Use **Environment setup** for missing values.
- Expose project-native commands for one decision cycle, continuous operation,
  tests, and an optional backtest when selected. Do not add a dry-run mode.
- Implement `fixed`, `dynamic`, or `constrained dynamic` selection. For runtime
  candidates without exact IDs, use `search_stocks`; reject missing or ambiguous
  results and never guess a mapping. Validate resolved IDs with `get_stocks`,
  batch when practical, and require the configured `stock` or `cryptocurrency`
  `security` type before ordering. Revalidate per the plan's freshness rule.
  Never order an invalid candidate; continue with valid candidates or abort as
  planned.
- Reconcile relevant AlphaInsider positions and open orders before decisions,
  validate its type at startup, and implement planned data, retry, duplicate,
  recovery, logging, sizing, and risk behavior. Never default a missing
  `input_multiplier` to `1`.
- Keep decisions testable. Backtests replay production logic chronologically
  without AlphaInsider calls or future information; reconstruct dynamic
  candidate sets without survivorship bias. Add portfolio accounting only with
  credible, documented execution and cost assumptions.
- Add offline tests for signals, risk, order mapping, orchestration, and any
  backtest; mock external services. Verification must never submit an order or
  run an order-submitting command.

Write `README.md` for humans with purpose, behavior, prerequisites, setup,
environment names, commands, monitoring, limitations, and recovery.
Include a short `## Start` section with ordered, copy-paste commands for
dependency installation and `.env` preparation. Label the exact commands for
one decision cycle and continuous operation equally. Match the selected
language and keep explanations brief. For Python, place
`source .venv/bin/activate` immediately before the execution commands. For any
other language, use the project's exact package-manager and runtime commands;
do not include Python steps.
Write `AGENTS.md` to make `docs/plan.md` authoritative, preserve the credential
boundary and missing-variable setup choices, identify code/test entry points,
and require maintenance below. Require agents to preserve `contract_version`,
follow Strategy Creator's installed-version workflow before behavior changes,
and never advance the version before applicable conformance and tests pass.

Run all offline tests and static checks. When code, tests, plan, and docs agree,
set `implemented`. Exclude deployment unless separately requested. Before
handoff, confirm every changed path is in the project and neither skill changed.

### Implemented

For behavior changes, return the plan to `draft`, interview affected decisions
one at a time, and reconfirm before code edits. Update code, tests, `README.md`,
and `AGENTS.md` together; restore `implemented` only after verification.
