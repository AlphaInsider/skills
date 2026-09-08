---
name: alphainsider-strategy-creator
description: Define, backtest, implement, schedule, resume, and update AlphaInsider paper strategies with a persistent project plan and optional automatic recovery.
---

# AlphaInsider Strategy Creator

Turn a strategy idea into working AlphaInsider paper automation. Use judgment
to choose relevant questions, guardrails, implementation, and checks for this
strategy. Keep the user's high-level decisions in charge of that judgment.

Read [workflow contracts](references/workflow-contracts.md) for the interview
and project continuity. Resume from the selected project's `plan.md` before
starting new work; keep all generated artifacts outside this skill repository.

## 1. Define strategy

Ask high-level questions until the intended behavior is clear enough to test
and implement. Research facts yourself and explain tradeoffs that affect the
user's choices. Decide which details need an answer and which you can choose.

Take the actual AI scheduler's capabilities, AlphaInsider constraints, data
availability, and other relevant limits into account before recommending a
strategy or cadence. Explain conflicts and offer feasible alternatives. Use
fixed code, scheduled AI judgment, or both as appropriate; record their roles.

For API behavior, read `alphainsider-api` when installed. Otherwise use the live
[documentation index](https://api.alphainsider.com/llms.txt), relevant focused
Markdown pages, and applicable [OpenAPI](https://api.alphainsider.com/openapi.yaml)
or [AsyncAPI](https://api.alphainsider.com/asyncapi.yaml) sections. Verify the
limits and side effects relevant to the intended actions rather than inventing
platform rules or copying an endpoint catalog into this skill.

## 2. Backtest

Assess whether the strategy can be tested with information available at each
historical decision time. Explain material limitations before asking backtest
questions. When a faithful test is unavailable, still offer the closest useful
options, such as a proxy, a signal-only test, or forward observation; explain
what each can establish. The user may choose a test, revise, or skip testing.

Ask the questions needed for the chosen test. Build and run it without
AlphaInsider orders. Save the methodology, assumptions, limitations, results,
and artifact links in the project and summarize them in `plan.md`. Clearly
identify approximations and future information; do not present them as a
faithful historical result.

Show understandable results and interpretation, with data-derived charts and
visuals when possible. Choose useful views for the test rather than a fixed
chart count. Save reproducible outputs and reports, including failures, and
let the user decide whether to revise, test further, implement, or stop.

## 3. Implement

1. Obtain AlphaInsider API access using [credentials](references/credentials.md).
   Accept deliberate chat entry and offer direct project `.env` editing.
   Verify access before proceeding to implementation questions.
2. Inspect compatible strategies the user owns. Recommend a new AlphaInsider
   strategy and offer existing strategies as options, explaining relevant
   existing state and effects of reuse. Ask the implementation questions that
   matter, including self-healing and notification preferences.
3. Build the program command and project-specific run instructions following
   [run and recover](references/run-and-recover.md). Support the agreed division
   of code and AI decisions, expected outcomes, persistent state, and one run
   at a time. Choose the remaining project structure to suit the implementation.
4. Verify the implementation with meaningful checks and a dry run that cannot
   submit, change, or cancel AlphaInsider orders. Make the selected setup and
   ongoing order, repair, and notification authority clear; use consent already
   given rather than requiring a special approval phrase.
5. Create or configure the selected AlphaInsider strategy and AI scheduled task,
   [activating it during setup](references/workflow-contracts.md#schedule-activation).
   Record resource identities and outcomes as they occur. Reconcile uncertain
   results before retrying resource creation or another external action.

Finish with the actual strategy and scheduler status, project location, useful
results, next scheduled run, and any required next action.
