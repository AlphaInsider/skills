# Strategy Plan

This file is the readable source of truth for the strategy. Keep it as a
concise record of decisions and authority, not a chat transcript. Replace
placeholders as decisions are made. Never record an API key, secret value, or
broker credential.

## Current status

- Creation state: In progress <!-- In progress | Stopped | Blocked | Complete -->
- Phase: Defining strategy <!-- Defining strategy | Assessing backtest | Planning backtest | Building backtest | Reviewing results | Planning implementation | Building implementation | Configuring automation | Complete -->
- Next step: Continue the strategy questions
- Waiting for: User answers
- Strategy status: Draft <!-- Draft | Confirmed -->
- Backtest status: Not started <!-- Not started | Draft | Authorized | Completed | Failed | Skipped -->
- AlphaInsider setup status: Not started <!-- Not started | Draft | Authorized | Active -->
- Highest completed outcome: None <!-- None | Strategy defined | Backtest | Automated strategy -->
- Automation state: Not configured <!-- Not configured | Active | Paused -->
- Automation state reason: _not applicable_ <!-- User | Update | Deletion | setup blocker -->
- Operational health: Not active <!-- Not active | Ready | Healthy | Degraded/Retrying -->
- Operational health detail and next retry: _not applicable_
- Creation state reason: _not applicable_ <!-- User stop | Technical blocker -->
- Last completed step: Project created from the stated objective
- Open questions: _not yet recorded_
- Last updated: _UTC timestamp_

## 1. Define strategy

### 1.1 Objective and market

- Goal: _not decided_
- Strategy type: _not decided_ <!-- stock | cryptocurrency -->
- Assets this strategy can trade: _not decided_
- How assets are selected: _not decided_ <!-- fixed list (fixed) | changes within defined limits (constrained dynamic) | changes anywhere within the strategy type (dynamic) -->
- Expected outcomes and known strategy limits: _not decided_

### 1.2 Decisions and evidence

- How decisions are made: _not decided_ <!-- fixed code (code-led) | AI decision (agent-led) | code and AI (hybrid) -->
- Signal and decision rules: _not decided_
- Information the AI can use, decisions it can make, limits, and output: _not applicable unless the strategy uses AI_
- Entry, exit, holding, and what to do when signal values are equal: _not decided_
- Required information and data cutoff: _not decided_
- Data sources, access, how recent data must be, and backup source: _not decided_
- What to do when information is missing, outdated, late, invalid, or conflicting: _not decided_

### 1.3 Execution and risk

- Planned AlphaInsider execution operation and material side effects: _not decided_
- AlphaInsider order type and size: _not decided_
- Maximum strategy exposure and execution-specific limit: _not decided_
- Position sizes, total amount invested, and loss limits: _not decided_
- Open orders, duplicate prevention, retries, and saved state: _not decided_
- Known account-tier dependency to verify during implementation: _none identified_

### 1.4 Timing and constraints

- Strategy schedule, timezone, daylight-saving behavior, and market-hours rules: _not decided_
- Native scheduler surface, supported timing limits, source, and checked time: _not checked_
- AlphaInsider public constraints, session policy and source, checked time, and unresolved documentation differences: _not checked_

## 2. Backtest strategy

### 2.1 Decision and feasibility

- Backtest choice: Not asked <!-- Not asked | Selected | Skipped -->
- Feasibility finding and recommended approach: _not assessed_
- Uses information unavailable at the historical decision time: Not assessed <!-- Not assessed | Yes | No -->
- Differences from intended automated execution and other limitations: _not decided_
- Limits and interpretation: _not decided_

### 2.2 Authorized design

- Data source, exact dataset, access, cost, and data cutoff: _not decided_
- Backtest period and decision times: _not decided_
- Order-fill, fee, estimated price difference (slippage), delay, and exposure assumptions: _not decided_
- Comparison investment (benchmark): _not decided_
- Results to show and charts: _not decided_ <!-- normally two to four data-derived visuals; plan two suitable substitutes for a signal-only backtest without portfolio results -->
- Checks that the backtest follows the strategy plan: _not decided_

### 2.3 Evidence and disposition

- Featured Valid result for the current strategy: _not run_
- Backtest run history, changes, future-information use, limitations, dispositions, source snapshots, and artifact paths: _not run_ <!-- include visual-rendering failures and later repairs -->

## 3. Implement and activate

### 3.1 Runtime design

- Scheduled strategy-run design: _not decided_
- Programming language, required software, and project files: _not decided_
- Strategy run and AI decision flow: _not decided_
- Saved state, one-run-at-a-time lock, run history, and how long records are kept: _not decided_
- Environment variable names and secret location: _not decided_
- AlphaInsider API access needed for setup and strategy runs: _not decided_
- Offline tests and expected results: _not decided_
- Managed files and external resources: _not decided_

### 3.2 AlphaInsider paper strategy

- Create a new or use an existing AlphaInsider strategy: _not decided_
- Existing AlphaInsider strategy reuse confirmation: _not applicable unless an existing strategy is selected_ <!-- confirmed | unresolved -->
- AlphaInsider strategy name: _not decided_
- AlphaInsider strategy description: _not decided_
- AlphaInsider simulated starting value: _not decided_
- AlphaInsider public or private setting: _not decided_ <!-- public | private -->
- AlphaInsider paid access and access price: _not applicable unless currently supported and selected_ <!-- free | paid with amount -->
- AlphaInsider strategy ID: _not assigned_
- AlphaInsider strategy URL: _not assigned_

### 3.3 Native automation

- Native AI scheduler and scheduled task name: _not decided_
- Schedule frequency, timezone, daylight-saving behavior, and missed runs: _not decided_
- One-run-at-a-time, Run now, chat run, and chat dry run behavior: _not decided_
- Operational error retry, reconciliation, and duplicate-notification behavior: _not decided_
- Self-healing: _not decided_ <!-- enabled | disabled -->
- What automatic repair can change, whether notification repair is in scope, what it must protect, how it undoes a failed repair, and time limit: _not applicable until enabled_
- Notifications: _not decided_ <!-- enabled | disabled -->
- Notification events, channels, and safe destination references: _not applicable until enabled_ <!-- errors only (recommended) | errors and completed repairs | errors, completed repairs, and warnings -->
- Notification support status for each selected channel: _not applicable until enabled_ <!-- supported | user-selected, unverified -->
- Future authority for AlphaInsider paper orders that follow this plan: _not decided_
