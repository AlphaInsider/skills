---
name: alphainsider-strategy-creator
description: Define, backtest, implement, schedule, resume, and update AlphaInsider paper strategies with a persistent project plan and optional automatic recovery.
---

# AlphaInsider Strategy Creator

## Start or resume

1. Run the [platform and automation access check](references/workflow-contracts.md#check-platform-and-automation-access)
   before [project setup](references/workflow-contracts.md#start-or-resume-the-project)
   or strategy work.
   - Resume from its `plan.md` before new work; keep generated artifacts outside
     this skill repository.
   - Let user decisions govern AlphaInsider paper automation.
   - Use judgment for questions, guardrails, implementation, and checks.
2. Continue from recorded state.
   - Handle stops and updates whenever requested.
   - Number required sequences; use bullets for other notes, ranked by importance
     at each level.

## Define strategy

1. Research strategy and cadence constraints.
   - Check actual AI scheduling capabilities, AlphaInsider constraints, data
     availability, and other relevant limits before recommending choices.
   - Explain conflicts, tradeoffs, and feasible alternatives.
   - Resolve relevant API behavior.
     - Read `alphainsider-api` when installed.
     - Otherwise use the live [documentation index](https://api.alphainsider.com/llms.txt),
       focused Markdown pages, and applicable
       [OpenAPI](https://api.alphainsider.com/openapi.yaml) or
       [AsyncAPI](https://api.alphainsider.com/asyncapi.yaml) sections.
     - Verify intended actions' limits and side effects; do not invent rules or
       copy endpoint catalogs.
2. [Ask high-level questions](references/workflow-contracts.md#resolve-the-current-decisions)
   until behavior is clear enough to test and implement.
   - Choose which details require user answers.
   - Use fixed code, scheduled AI judgment, or both; record their roles.
3. [Review the strategy and choose the next phase](references/workflow-contracts.md#choose-the-next-phase).

## Backtest

1. Assess feasibility before asking backtest questions.
   - Check information availability at each historical decision time.
   - Explain material limitations. When faithful testing is unavailable, offer
     the closest useful alternatives (proxy, signal-only test, forward observation)
     and what each can establish.
2. Ask backtest questions; let the user choose a test, revise, or skip testing.
3. Build and run the chosen test.
   - Submit no AlphaInsider orders.
   - Identify approximations and future information; do not portray them as
     faithful historical results.
4. Save and present results.
   - Save methodology, assumptions, limitations, results, reproducible outputs,
     reports including failures, and artifact links; summarize them in `plan.md`.
   - Explain results clearly with useful data-derived charts and visuals when
     possible; avoid a fixed chart count.
5. [Review the results and choose the next phase](references/workflow-contracts.md#choose-the-next-phase).

## Implement

1. Obtain and verify API access through [credentials](references/credentials.md).
   - Accept deliberate chat entry or direct project `.env` editing.
   - Complete any required user-action turn before implementation questions.
2. Ask relevant implementation questions.
   - Recommend a new public strategy (`private: false`). Inspect and offer
     compatible owned strategies, explaining their state and reuse effects.
   - Resolve self-healing and notification preferences.
3. Build the program command and runbook using
   [run and recover](references/run-and-recover.md).
   - Support agreed code/AI roles, expected outcomes, persistent state, and one
     run at a time; choose the remaining project structure.
4. Verify implementation and establish setup scope.
   - Use meaningful checks and a dry run unable to submit, change, or cancel orders.
   - Clarify setup and ongoing order, repair, and notification authority; honor
     existing consent without a special approval phrase.
5. Create or configure the AlphaInsider strategy and selected scheduled task.
   - [Activate during setup](references/workflow-contracts.md#activate-the-schedule).
   - Record identities and outcomes as they occur; reconcile uncertain results
     before retrying resource creation or another external action.
6. Hand off actual strategy/scheduler status, project location, useful results,
   next scheduled run, and any required next action.

## Run and recover

- Follow current `plan.md` and the generated runbook for scheduled or manual runs.
  - The [runtime workflow](references/run-and-recover.md) covers execution,
    evaluation, recovery, and notifications.
