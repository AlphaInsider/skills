# Strategy Plan

This file is the readable source of truth for the strategy. Keep it as a
concise record of agreed decisions, not a chat transcript. Replace placeholders
as decisions are made. Never record an API key, secret value, or broker
credential.

## Strategy plan

- Goal: _not decided_
- Strategy type: _not decided_ <!-- stock | cryptocurrency -->
- Assets this strategy can trade: _not decided_
- How assets are selected: _not decided_ <!-- fixed list (fixed) | changes within agreed limits (constrained dynamic) | changes anywhere within the strategy type (dynamic) -->
- How decisions are made: _not decided_ <!-- fixed code (code-led) | AI decision (agent-led) | code and AI (hybrid) -->
- Required information and data cutoff: _not decided_
- Data sources, access, how recent data must be, and backup source: _not decided_
- Signal and decision rules: _not decided_
- Information the AI can use, decisions it can make, limits, and output: _not applicable unless the strategy uses AI_
- Entry, exit, holding, and what to do when signal values are equal: _not decided_
- AlphaInsider order type and size: _not decided_
- Maximum strategy leverage: _not decided_ <!-- AlphaInsider permits up to 2×; this is a ceiling, not a goal -->
- Position sizes, total amount invested, and loss limits: _not decided_
- Open orders, duplicate prevention, retries, and saved state: _not decided_
- What to do when information is missing, outdated, late, invalid, or conflicting: _not decided_
- Strategy schedule, timezone, daylight-saving behavior, and market-hours rules: _not decided_
- Expected outcomes and known strategy limits: _not decided_

## Backtesting plan

- User choice: _not asked_ <!-- accepted | declined | unavailable -->
- Recreating past decisions without future information: _not decided_
- Data source, exact dataset, and data cutoff: _not decided_
- Test period and decision times: _not decided_
- Order-fill, fee, estimated price difference (slippage), delay, and leverage assumptions: _not decided_
- Comparison investment (benchmark): _not decided_
- Results to show and charts: _not decided_
- Checks that the backtest follows the strategy plan: _not decided_
- Results: _not run_
- Limits and interpretation: _not decided_

## AlphaInsider setup plan

- Scheduled strategy-run design: _not decided_
- Programming language, required software, and project files: _not decided_
- Strategy run and AI decision flow: _not decided_
- Saved state, one-run-at-a-time lock, run history, and how long records are kept: _not decided_
- Environment variable names and secret location: _not decided_
- AlphaInsider API access needed for setup and strategy runs: _not decided_
- Create a new or use an existing AlphaInsider strategy: _not decided_
- Existing AlphaInsider strategy reuse confirmation: _not applicable unless an existing strategy is selected_ <!-- confirmed | unresolved -->
- AlphaInsider strategy name: _not decided_
- AlphaInsider simulated starting value: _not decided_
- AlphaInsider public or private setting: _not decided_ <!-- public | private -->
- AlphaInsider paid access and access price: _not applicable unless currently supported and selected_ <!-- free | paid with amount -->
- AlphaInsider strategy ID: _not assigned_
- AlphaInsider strategy URL: _not assigned_
- AlphaInsider strategy description: _not decided_
- Native AI scheduler and scheduled task name: _not decided_
- Schedule frequency, timezone, daylight-saving behavior, and missed runs: _not decided_
- One-run-at-a-time, Run now, chat run, and chat dry run behavior: _not decided_
- Self-healing: _not decided_ <!-- enabled | disabled -->
- What automatic repair can change, what it must protect, how it undoes a failed repair, and time limit: _not applicable until enabled_
- Notifications: _not decided_ <!-- enabled | disabled -->
- Notification events, channels, and safe destination references: _not applicable until enabled_ <!-- errors only (recommended) | errors and completed repairs | errors, completed repairs, and warnings -->
- Offline tests and expected results: _not decided_
- Future authority for AlphaInsider paper orders that follow this plan: _not decided_
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
