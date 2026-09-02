# Strategy Plan

This file is the readable source of truth for the strategy. Keep it as a
normalized agreement, not a chat transcript. Replace placeholders as decisions
are made. Never record an API key, secret value, or broker credential.

## Strategy plan

- Goal: _not decided_
- Strict asset class: _not decided_ <!-- stock | cryptocurrency -->
- Instrument universe: _not decided_
- Selection method and type boundary: _not decided_ <!-- fixed | dynamic | constrained dynamic -->
- Decision mode: _not decided_ <!-- code-led | agent-led | hybrid -->
- Required inputs and as-of timing: _not decided_
- Data sources, access, freshness, and fallback: _not decided_
- Signal and decision rules: _not decided_
- Agent discretion inputs, allowed judgments, limits, and output: _not applicable unless agent-led or hybrid_
- Entry, exit, holding, and tie-break rules: _not decided_
- AlphaInsider order method and sizing: _not decided_
- Maximum strategy leverage: _not decided_ <!-- AlphaInsider permits up to 2×; this is a ceiling, not a target -->
- Position, exposure, and loss controls: _not decided_
- Open-order, duplicate-event, retry, and reconciliation rules: _not decided_
- Missing, stale, late, invalid, or conflicting input behavior: _not decided_
- High-level cadence, timezone, DST behavior, and market-hours rules: _not decided_
- Expected outcomes and known strategy limits: _not decided_

## Backtesting plan

- User choice: _not asked_ <!-- accepted | declined | unavailable -->
- Historical reconstruction and future-data controls: _not decided_
- Data source, dataset identity, and data as-of time: _not decided_
- Window and decision timestamps: _not decided_
- Fill, fee, slippage, latency, and leverage assumptions: _not decided_
- Benchmark: _not decided_
- Metrics and charts: _not decided_
- Plan-conformance checks: _not decided_
- Results: _not run_
- Limits and interpretation: _not decided_

## Implementation plan

- Forward-test design: _not decided_
- Language, dependencies, and project structure: _not decided_
- Finite-cycle or agent-decision flow: _not decided_
- Persistent state, lock, run history, and retention: _not decided_
- Environment variable names and secret location: _not decided_
- AlphaInsider API permission plan: _not decided_
- AlphaInsider target choice and source: _not decided_ <!-- create new | compatible owned target -->
- AlphaInsider strategy name, access, and paper starting balance: _not decided_
- AlphaInsider strategy ID: _not assigned_
- AlphaInsider strategy URL: _not assigned_
- Generated AlphaInsider description: _not decided_
- Native AI scheduler provider and task identity: _not decided_
- Supported cadence, timezone, DST, and missed-run behavior: _not decided_
- Overlap, Run now, chat normal-run, and chat dry-run behavior: _not decided_
- Self-healing: _not decided_ <!-- enabled | disabled -->
- Repair scope, protected resources, rollback, and time limit: _not applicable until enabled_
- Notifications: _not decided_ <!-- enabled | disabled -->
- Notification channel, destination, and event policy: _not applicable until enabled_
- Offline tests and expected evidence: _not decided_
- Future plan-conforming paper-order authority: _not decided_
- Managed files and external resources: _not decided_

## Current status

- Phase: Interviewing <!-- Interviewing | Building backtest | Reviewing results | Building implementation | Configuring automation | Complete -->
- Plan agreement: Draft <!-- Draft | Agreed -->
- Highest completed outcome: None <!-- None | Plan | Backtest | Automated strategy -->
- Automation state: Not configured <!-- Not configured | Active | Paused -->
- Automation state reason: _not applicable_ <!-- User | Error | Update | Deletion | setup blocker -->
- Last completed step: Project created from the stated objective
- Next step: Continue the strategy interview
- Waiting for: User answers
- Open questions: _not yet recorded_
- Last updated: _UTC timestamp_
