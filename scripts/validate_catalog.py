#!/usr/bin/env python3
"""Validate the public AlphaInsider skill catalog."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
EXPECTED_SKILLS = {
    "alphainsider",
    "alphainsider-api",
    "alphainsider-strategy-creator",
}
WRAPPER_NAME = "alphainsider"
EXPECTED_WRAPPER_REFERENCES = {
    "catalog.md",
}
EXPECTED_WRAPPER_SCRIPTS: set[str] = set()
REQUIRED_WRAPPER_TRIGGERS = {
    "/alphainsider",
    "use the alphainsider skill",
    "route this with alphainsider",
    "which AlphaInsider skill",
}
REQUIRED_WRAPPER_GUIDANCE = {
    "references/catalog.md",
    "always ask",
    "npx skills list",
    "npx skills@latest use",
    "Never pass `--agent`",
    "only when the user asks",
    "recommend global",
    "--skill <name> -g -y",
    "Do not require any specialist",
}
CATALOG_HEADING_PATTERN = re.compile(
    r"^## ([a-z0-9]+(?:-[a-z0-9]+)*)$", re.MULTILINE
)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
URI_SCHEME_PATTERN = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
EXPECTED_ALPHA_SCRIPTS = {
    "alphainsider_request.py",
    "alphainsider_stream.py",
}
EXPECTED_ALPHA_REFERENCES = {
    "api-reference.md",
    "authentication.md",
    "bots.md",
    "input-multiplier.md",
    "limits.md",
    "payments.md",
    "stocks.md",
    "strategies.md",
    "subscriptions.md",
    "timelines.md",
    "trades.md",
    "users.md",
    "webhooks.md",
    "websockets.md",
    "withdrawals.md",
}
EXPECTED_ALPHA_REST_SECTIONS = {
    "authentication.md": (
        ("verifyToken", "GET", "/verifyToken"),
    ),
    "users.md": (
        ("getUsers", "GET", "/getUsers"),
        ("getUserInfo", "GET", "/getUserInfo"),
        ("updateUserInfo", "POST", "/updateUserInfo"),
        ("updateUserNotifications", "POST", "/updateUserNotifications"),
    ),
    "strategies.md": (
        ("getStrategies", "GET", "/getStrategies"),
        ("getStrategyValues", "GET", "/getStrategyValues"),
        ("getUserStrategies", "GET", "/getUserStrategies"),
        ("getStrategyPerformance", "GET", "/getStrategyPerformance"),
        ("getRecommendedStrategies", "GET", "/getRecommendedStrategies"),
        ("searchStrategies", "POST", "/searchStrategies"),
        ("newStrategy", "POST", "/newStrategy"),
        ("updateStrategy", "POST", "/updateStrategy"),
        ("updateStrategyPrice", "POST", "/updateStrategyPrice"),
        ("deleteStrategy", "POST", "/deleteStrategy"),
    ),
    "subscriptions.md": (
        ("getStrategySubscriptions", "GET", "/getStrategySubscriptions"),
        ("newStrategySubscription", "POST", "/newStrategySubscription"),
        ("deleteStrategySubscription", "POST", "/deleteStrategySubscription"),
        (
            "updateStrategySubscriptionNotifications",
            "POST",
            "/updateStrategySubscriptionNotifications",
        ),
        ("getStrategyCalculation", "GET", "/getStrategyCalculation"),
        ("updateStrategyCalculation", "POST", "/updateStrategyCalculation"),
        ("deleteStrategyCalculation", "POST", "/deleteStrategyCalculation"),
        ("getAccountTiers", "GET", "/getAccountTiers"),
        ("getAccountSubscription", "GET", "/getAccountSubscription"),
        ("updateAccountSubscription", "POST", "/updateAccountSubscription"),
    ),
    "payments.md": (
        ("getPaymentSources", "GET", "/getPaymentSources"),
        ("getUpcomingInvoice", "GET", "/getUpcomingInvoice"),
        ("getInvoices", "GET", "/getInvoices"),
        ("getInvoicePdf", "GET", "/getInvoicePdf"),
        ("retryInvoice", "POST", "/retryInvoice"),
        ("getUpcomingInvoiceItems", "GET", "/getUpcomingInvoiceItems"),
        ("getInvoiceItems", "GET", "/getInvoiceItems"),
    ),
    "withdrawals.md": (
        ("getUserBalance", "GET", "/getUserBalance"),
        ("getPayouts", "GET", "/getPayouts"),
        ("newPayout", "POST", "/newPayout"),
        ("getPayoutFees", "GET", "/getPayoutFees"),
        ("getIncome", "GET", "/getIncome"),
        ("getStripeAccountLink", "GET", "/getStripeAccountLink"),
    ),
    "timelines.md": (
        ("getTimelines", "GET", "/getTimelines"),
        ("getStrategyTimelines", "GET", "/getStrategyTimelines"),
        ("newPost", "POST", "/newPost"),
        ("previewPost", "POST", "/previewPost"),
        ("deletePost", "POST", "/deletePost"),
        ("like", "POST", "/like"),
        ("unlike", "POST", "/unlike"),
    ),
    "stocks.md": (
        ("getStocks", "GET", "/getStocks"),
        ("getAllStocks", "GET", "/getAllStocks"),
        ("getStockPriceHistory", "GET", "/getStockPriceHistory"),
        ("searchStocks", "POST", "/searchStocks"),
        ("getExchangeStatus", "GET", "/getExchangeStatus"),
    ),
    "trades.md": (
        ("getPositions", "GET", "/getPositions"),
        ("getOrders", "GET", "/getOrders"),
        ("getMaxOrderSize", "GET", "/getMaxOrderSize"),
        ("newOrder", "POST", "/newOrder"),
        ("newOrderAllocations", "POST", "/newOrderAllocations"),
        ("deleteOrder", "POST", "/deleteOrder"),
    ),
    "bots.md": (
        ("getBots", "GET", "/getBots"),
        ("getBotInfo", "GET", "/getBotInfo"),
        ("newBot", "POST", "/newBot"),
        ("updateBotSettings", "POST", "/updateBotSettings"),
        ("updateBotBrokerKeys", "POST", "/updateBotBrokerKeys"),
        ("updateBotNotifications", "POST", "/updateBotNotifications"),
        ("deleteBot", "POST", "/deleteBot"),
        ("startBot", "POST", "/startBot"),
        ("stopBot", "POST", "/stopBot"),
        ("resetBot", "POST", "/resetBot"),
        ("getBotPerformance", "GET", "/getBotPerformance"),
        ("resetBotPerformance", "POST", "/resetBotPerformance"),
        ("getBotAllocations", "GET", "/getBotAllocations"),
        ("updateBotAllocations", "POST", "/updateBotAllocations"),
        ("getBotActivities", "GET", "/getBotActivities"),
    ),
    "webhooks.md": (
        ("newOrderWebhook", "POST", "/newOrderWebhook"),
    ),
}
EXPECTED_ALPHA_WEBSOCKET_SECTIONS = (
    ("ping", "Ping"),
    ("pingResponse", "Ping Response"),
    ("subscribe", "Subscribe"),
    ("subscribeResponse", "Subscribe Response"),
    ("error", "Error Response"),
    ("wsStockPrice", "Stock Price"),
    ("wsStrategyValue", "Strategy Value"),
    ("wsOrders", "Orders"),
    ("wsPositions", "Positions"),
    ("wsTimelines", "Timelines"),
    ("wsBotStatus", "Bot Status"),
    ("wsBotAllocations", "Bot Allocations"),
    ("wsBotActivities", "Bot Activities"),
)
EXPECTED_STRATEGY_REFERENCES = {
    "backtest-strategy.md",
    "define-strategy.md",
    "delete-strategy.md",
    "implement-and-activate.md",
    "plan-template.md",
    "project-contract.md",
    "run-and-recover.md",
    "start-or-resume.md",
    "update-strategy.md",
    "workflow-contracts.md",
}
EXPECTED_STRATEGY_SCRIPTS = {
    "alphainsider_setup_request.py",
    "set_env_value.py",
}
STRATEGY_SKILL_MAX_WORDS = 700
REQUIRED_PLAN_SECTION_ORDER = (
    "# Strategy Plan",
    "## Current status",
    "## 1. Define strategy",
    "## 2. Backtest strategy",
    "## 3. Implement and activate",
)
REQUIRED_PLAN_FIELD_LINES = (
    "- Creation state: In progress <!-- In progress | Stopped | Blocked | Complete -->",
    "- Phase: Defining strategy <!-- Defining strategy | Assessing backtest | Planning backtest | Building backtest | Reviewing results | Planning implementation | Building implementation | Configuring automation | Complete -->",
    "- Next step: Continue the strategy questions",
    "- Waiting for: User answers",
    "- Strategy status: Draft <!-- Draft | Confirmed -->",
    "- Backtest status: Not started <!-- Not started | Draft | Authorized | Completed | Failed | Skipped -->",
    "- AlphaInsider setup status: Not started <!-- Not started | Draft | Authorized | Active -->",
    "- Highest completed outcome: None <!-- None | Strategy defined | Backtest | Automated strategy -->",
    "- Automation state: Not configured <!-- Not configured | Active | Paused -->",
    "- Automation state reason: _not applicable_ <!-- User | Update | Deletion | setup blocker -->",
    "- Operational health: Not active <!-- Not active | Ready | Healthy | Degraded/Retrying -->",
    "- Operational health detail and next retry: _not applicable_",
    "- Creation state reason: _not applicable_ <!-- User stop | Technical blocker -->",
    "- Last completed step: Project created from the stated objective",
    "- Open questions: _not yet recorded_",
    "- Last updated: _UTC timestamp_",
    "- Goal: _not decided_",
    "- Strategy type: _not decided_ <!-- stock | cryptocurrency -->",
    "- Assets this strategy can trade: _not decided_",
    "- How assets are selected: _not decided_ <!-- fixed list (fixed) | changes within defined limits (constrained dynamic) | changes anywhere within the strategy type (dynamic) -->",
    "- Expected outcomes and known strategy limits: _not decided_",
    "- How decisions are made: _not decided_ <!-- fixed code (code-led) | AI decision (agent-led) | code and AI (hybrid) -->",
    "- Signal and decision rules: _not decided_",
    "- Information the AI can use, decisions it can make, limits, and output: _not applicable unless the strategy uses AI_",
    "- Entry, exit, holding, and what to do when signal values are equal: _not decided_",
    "- Required information and data cutoff: _not decided_",
    "- Data sources, access, how recent data must be, and backup source: _not decided_",
    "- What to do when information is missing, outdated, late, invalid, or conflicting: _not decided_",
    "- Planned AlphaInsider execution operation and material side effects: _not decided_",
    "- AlphaInsider order type and size: _not decided_",
    "- Maximum strategy exposure and execution-specific limit: _not decided_",
    "- Position sizes, total amount invested, and loss limits: _not decided_",
    "- Open orders, duplicate prevention, retries, and saved state: _not decided_",
    "- Known account-tier dependency to verify during implementation: _none identified_",
    "- Strategy schedule, timezone, daylight-saving behavior, and market-hours rules: _not decided_",
    "- Native scheduler surface, supported timing limits, source, and checked time: _not checked_",
    "- AlphaInsider public constraints, session policy and source, checked time, and unresolved documentation differences: _not checked_",
    "- Backtest choice: Not asked <!-- Not asked | Selected | Skipped -->",
    "- Feasibility finding and recommended approach: _not assessed_",
    "- Uses information unavailable at the historical decision time: Not assessed <!-- Not assessed | Yes | No -->",
    "- Differences from intended automated execution and other limitations: _not decided_",
    "- Limits and interpretation: _not decided_",
    "- Data source, exact dataset, access, cost, and data cutoff: _not decided_",
    "- Backtest period and decision times: _not decided_",
    "- Order-fill, fee, estimated price difference (slippage), delay, and exposure assumptions: _not decided_",
    "- Comparison investment (benchmark): _not decided_",
    "- Results to show and charts: _not decided_ <!-- normally two to four data-derived visuals; plan two suitable substitutes for a signal-only backtest without portfolio results -->",
    "- Checks that the backtest follows the strategy plan: _not decided_",
    "- Featured Valid result for the current strategy: _not run_",
    "- Backtest run history, changes, future-information use, limitations, dispositions, source snapshots, and artifact paths: _not run_ <!-- include visual-rendering failures and later repairs -->",
    "- Scheduled strategy-run design: _not decided_",
    "- Programming language, required software, and project files: _not decided_",
    "- Strategy run and AI decision flow: _not decided_",
    "- Saved state, one-run-at-a-time lock, run history, and how long records are kept: _not decided_",
    "- Environment variable names and secret location: _not decided_",
    "- AlphaInsider API access needed for setup and strategy runs: _not decided_",
    "- Offline tests and expected results: _not decided_",
    "- Managed files and external resources: _not decided_",
    "- Create a new or use an existing AlphaInsider strategy: _not decided_",
    "- Existing AlphaInsider strategy reuse confirmation: _not applicable unless an existing strategy is selected_ <!-- confirmed | unresolved -->",
    "- AlphaInsider strategy name: _not decided_",
    "- AlphaInsider strategy description: _not decided_",
    "- AlphaInsider simulated starting value: _not decided_",
    "- AlphaInsider public or private setting: _not decided_ <!-- public | private -->",
    "- AlphaInsider paid access and access price: _not applicable unless currently supported and selected_ <!-- free | paid with amount -->",
    "- AlphaInsider strategy ID: _not assigned_",
    "- AlphaInsider strategy URL: _not assigned_",
    "- Native AI scheduler and scheduled task name: _not decided_",
    "- Schedule frequency, timezone, daylight-saving behavior, and missed runs: _not decided_",
    "- One-run-at-a-time, Run now, chat run, and chat dry run behavior: _not decided_",
    "- Operational error retry, reconciliation, and duplicate-notification behavior: _not decided_",
    "- Self-healing: _not decided_ <!-- enabled | disabled -->",
    "- What automatic repair can change, whether notification repair is in scope, what it must protect, how it undoes a failed repair, and time limit: _not applicable until enabled_",
    "- Notifications: _not decided_ <!-- enabled | disabled -->",
    "- Notification events, channels, and safe destination references: _not applicable until enabled_ <!-- errors only (recommended) | errors and completed repairs | errors, completed repairs, and warnings -->",
    "- Notification support status for each selected channel: _not applicable until enabled_ <!-- supported | user-selected, unverified -->",
    "- Future authority for AlphaInsider paper orders that follow this plan: _not decided_",
)
REQUIRED_STRATEGY_OUTLINE_HEADINGS = {
    "SKILL.md": (
        "## Contract",
        "## 1. Start or resume",
        "## 2. Route the request",
        "### Create or complete a strategy",
        "### Operate the strategy",
        "### Update the strategy",
        "### Delete strategy resources",
    ),
    "references/workflow-contracts.md": (
        "## Apply confirmation and action authority",
        "## Maintain the plan and lifecycle state",
        "## Ask each available decision round",
        "## Review and advance a decision stage",
        "## Stop, block, and resume creation",
        "## Resolve AlphaInsider API behavior",
        "## Request a user action",
        "## Communicate outcomes and notifications",
        "## Prepare each user-facing turn",
    ),
    "references/start-or-resume.md": (
        "## 1. Select a persistent parent",
        "## 2. Find a matching project",
        "## 3. Resolve the project",
        "### Create a project when needed",
        "### Resume an existing project",
        "## 4. Route the work",
    ),
    "references/project-contract.md": (
        "## Maintain the plan contract",
        "## Create and maintain the workspace",
        "## Prove durable automation access",
        "## Migrate an older plan schema",
        "## Generate scheduled-run instructions",
        "## Generate the project agent guide",
        "## Generate the human README",
        "## Hand off incomplete creation",
        "## Hand off completed automation",
    ),
    "references/define-strategy.md": (
        "## 1. Enter definition",
        "## 2. Define the objective and market",
        "## 3. Define behavior and decision responsibility",
        "## 4. Resolve data, execution, and risk",
        "### Direct order",
        "### Complete target allocation",
        "### Signal-style webhook",
        "## 5. Discover native timing capabilities",
        "### Stock session policy",
        "### Cryptocurrency availability",
        "## 6. Select complete timing behavior",
        "## 7. Review the strategy and route forward",
    ),
    "references/backtest-strategy.md": (
        "## 1. Enter backtesting",
        "## 2. Assess feasibility",
        "### 2.1 Choose a feasible method",
        "## 3. Plan the backtest",
        "### 3.1 Plan result visuals",
        "## 4. Review and authorize the plan",
        "## 5. Build and execute an authorized run",
        "### 5.1 Classify the run",
        "### 5.2 Preserve and repair visuals",
        "### 5.3 Manage later runs and revisions",
        "## 6. Present results",
        "### 6.1 Show measurements",
        "### 6.2 Show saved visual evidence",
        "## 7. Record status and choose the next step",
    ),
    "references/implement-and-activate.md": (
        "## 1. Enter implementation planning",
        "## 2. Establish protected configuration",
        "### 2.1 Select secret storage",
        "### 2.2 Collect a missing API key",
        "### 2.3 Verify API access privately",
        "## 3. Select an AlphaInsider paper strategy",
        "### 3.1 Discover compatible owned strategies",
        "### 3.2 Resolve the selected path",
        "#### Reuse an owned strategy",
        "#### Create a new paper strategy",
        "## 4. Design implementation and native automation",
        "### 4.1 Map the decision mode",
        "### 4.2 Recheck the native scheduler",
        "### 4.3 Configure self-healing",
        "### 4.4 Configure notifications",
        "### 4.5 Reconcile backtest disclosures",
        "## 5. Review and authorize setup",
        "## 6. Build the authorized implementation",
        "## 7. Implement the shared compatibility gate",
        "## 8. Pass offline, order-free verification",
        "## 9. Create or revalidate the paper strategy",
        "## 10. Configure and activate native automation",
        "## 11. Complete creation",
    ),
    "references/run-and-recover.md": (
        "## 1. Classify the trigger",
        "## 2. Acquire the shared lock",
        "## 3. Admit one strategy run",
        "## 4. Execute the confirmed strategy",
        "## 5. Evaluate operational health",
        "## 6. Respond to an operational error",
        "### When self-healing is enabled",
        "### When self-healing is disabled",
        "## 7. Recover on a later trigger",
        "## Send runtime notifications",
    ),
    "references/update-strategy.md": (
        "## 1. Classify the change",
        "### External drift",
        "## 2. Isolate a proposed behavior change",
        "## 3. Redefine only affected behavior",
        "## 4. Reconcile affected backtests",
        "## 5. Review and authorize implementation changes",
        "## 6. Apply and finalize the update",
    ),
    "references/delete-strategy.md": (
        "## 1. Inventory attributable resources",
        "## 2. Select deletion scope",
        "## 3. Review exact effects",
        "## 4. Pause safely",
        "## 5. Apply confirmed deletion",
        "## 6. Record the outcome",
    ),
    "references/plan-template.md": (
        "## Current status",
        "## 1. Define strategy",
        "### 1.1 Objective and market",
        "### 1.2 Decisions and evidence",
        "### 1.3 Execution and risk",
        "### 1.4 Timing and constraints",
        "## 2. Backtest strategy",
        "### 2.1 Decision and feasibility",
        "### 2.2 Authorized design",
        "### 2.3 Evidence and disposition",
        "## 3. Implement and activate",
        "### 3.1 Runtime design",
        "### 3.2 AlphaInsider paper strategy",
        "### 3.3 Native automation",
    ),
}

REQUIRED_STRATEGY_LINKS = {
    "SKILL.md": {
        "references/workflow-contracts.md",
        "references/start-or-resume.md",
        "references/project-contract.md",
        "references/plan-template.md",
        "references/define-strategy.md",
        "references/backtest-strategy.md",
        "references/implement-and-activate.md",
        "references/run-and-recover.md",
        "references/update-strategy.md",
        "references/delete-strategy.md",
    },
    "references/start-or-resume.md": {
        "references/workflow-contracts.md",
        "references/project-contract.md",
        "references/plan-template.md",
        "references/define-strategy.md",
        "references/backtest-strategy.md",
        "references/implement-and-activate.md",
        "references/run-and-recover.md",
        "references/update-strategy.md",
        "references/delete-strategy.md",
    },
    "references/update-strategy.md": {
        "references/define-strategy.md",
        "references/backtest-strategy.md",
        "references/implement-and-activate.md",
        "references/delete-strategy.md",
    },
}

# Stable user-facing labels, paths, values, and links remain exact. Behavioral
# checks below use compact concept fragments rather than sentence-shaped prose.
REQUIRED_STRATEGY_LITERALS = {
    "references/workflow-contracts.md": {
        "ASD-STE100-style technical English",
        "👉 **Action — Short title:**",
        "💡 **Optional next step — Short title:**",
        "`⚠️ Warning — No Action Required`",
        "`🔄 Retrying — No Action Required`",
        "`🛠️ Self-Healed — No Action Required`",
        "`🚨 Error — Action Required`",
    },
    "references/define-strategy.md": {
        "**Backtest Strategy**",
        "**Skip Backtesting and Implement on AlphaInsider**",
        "`newOrder`",
        "`newOrderAllocations`",
        "`newOrderWebhook`",
        "`2×`",
        "`1×`",
        "09:30",
        "16:00",
        "`America/New_York`",
    },
    "references/backtest-strategy.md": {
        "**Build and Run**",
        "Backtest <date or ID>",
        "**Valid**",
        "**Superseded**",
        "**Failed**",
    },
    "references/implement-and-activate.md": {
        "scripts/set_env_value.py",
        "scripts/alphainsider_setup_request.py",
        "https://alphainsider.com/settings/developers",
        "`$100,000`",
        "**Build, Configure, and Activate**",
        "**Errors only**",
        "**Errors and completed repairs**",
        "**Errors, completed repairs, and warnings**",
        "scheduler **Run now**",
    },
    "references/run-and-recover.md": {
        "30 minutes",
        "scheduler **Run now**",
    },
    "references/project-contract.md": {
        "Creation incomplete",
        "Strategy created successfully",
        "Strategy automation completed successfully",
        "plan-before-schema-migration-YYYYMMDDTHHMMSSZ.md",
        "https://alphainsider.com/resources#automating-trades",
    },
    "references/delete-strategy.md": {
        "**Delete everything**",
    },
}

FORBIDDEN_STRATEGY_LITERALS = {
    "references/workflow-contracts.md": {
        "Agree to this strategy",
        "Agree to this backtest plan",
        "Agree to this AlphaInsider setup",
        "Finish here",
    },
    "references/define-strategy.md": {
        "AlphaInsider permits up to `2×` leverage",
    },
    "references/implement-and-activate.md": {
        "Attempt a non-trading delivery check",
        "notification delivery has been attempted",
    },
    "references/plan-template.md": {
        "- Maximum strategy leverage:",
    },
}

FORBIDDEN_BACKTEST_NAME_PATTERNS = {
    "retired test alias": re.compile(
        r"\bhistorical(?:-|\s+)test(?:s|ing)?\b", re.IGNORECASE
    ),
    "hindsight": re.compile(r"\bhindsight\b", re.IGNORECASE),
}

REQUIRED_STRATEGY_CONCEPTS = {
    "SKILL.md": {
        "paper-only boundary": (
            "paper strategies",
            "broker credentials",
        ),
        "plan authority": (
            "`plan.md`",
            "source of truth",
        ),
        "one strict asset type": (
            "one strict",
            "`stock`",
            "`cryptocurrency`",
        ),
        "native scheduling only": (
            "native ai",
            "host scheduler",
            "faster cadence",
        ),
        "operational errors keep automation active": (
            "degraded/retrying",
            "next trigger",
            "pause",
        ),
        "completion requires active automation": (
            "creation complete",
            "native automation is active",
        ),
    },
    "references/workflow-contracts.md": {
        "draft permits safe discovery": (
            "draft strategy",
            "interviewing",
            "read-only discovery",
        ),
        "review and choice share one prompt": (
            "same prompt",
            "forward choice",
            "separate agreement",
        ),
        "build choices gate authority": (
            "only **build and run**",
            "only **build, configure, and activate**",
            "authorized",
        ),
        "stops remain incomplete": (
            "never set phase or creation state to complete",
            "stopped",
            "blocked",
        ),
        "poor performance is not health": (
            "poor profit",
            "not a lifecycle or health transition",
        ),
        "material choices explain tradeoffs": (
            "material tradeoff",
            "offered choices",
        ),
    },
    "references/start-or-resume.md": {
        "persistent storage outlives chat": (
            "outlive this chat",
            "new chat",
            "do not ask the user where",
        ),
        "project discovery avoids secrets": (
            "do not crawl unrelated source",
            "open `.env`",
        ),
        "multiple matches require a choice": (
            "several projects match",
            "**create a new strategy**",
        ),
        "ambiguous work is reconciled": (
            "ambiguous or partial external outcome",
            "never create a replacement",
        ),
        "former flat plans stay compatible": (
            "accept both the new ranked layout",
            "former flat section layout",
        ),
    },
    "references/project-contract.md": {
        "legacy migration is recoverable": (
            "exact contents",
            "collision-safe suffix",
            "never overwrite a prior backup",
        ),
        "legacy work is not promoted": (
            "never promote ambiguous work",
            "authorized, active, or complete",
        ),
        "complete state is cross-field verified": (
            "phase is complete",
            "alphaInsider setup status is active",
            "automation state is active",
            "operational health is ready or healthy",
        ),
        "runtime errors preserve completed creation": (
            "later operational error preserves creation state",
            "degraded/retrying",
        ),
        "generated handoffs present saved visuals": (
            "reuse the exact saved visuals",
            "embed them when supported",
            "link directly to each named image",
            "detailed report is additional",
        ),
    },
    "references/define-strategy.md": {
        "operation is mapped internally": (
            "internally map",
            "do not ask the user to choose an endpoint",
        ),
        "allocation side effects are disclosed": (
            "`neworderallocations`",
            "cancels existing open orders",
            "closes positions omitted",
        ),
        "exposure is operation-specific": (
            "`neworder` has no leverage field",
            "no documented universal `2×`",
            "`getmaxordersize`",
        ),
        "stock sessions use documented rule or fallback": (
            "explicit current accepted-session rule",
            "strategy creator fallback",
            "u.s. stock-market trading day",
        ),
        "cryptocurrency availability is continuous": (
            "cryptocurrency order availability as 24/7",
            "do not ask a cryptocurrency market-session question",
        ),
        "unsupported timing has no workaround": (
            "offer the nearest complete supported alternatives",
            "never offer submission with an expected rejection",
            "saved signal without a supported execution time",
        ),
        "backtesting is always offered first": (
            "always show this choice",
            "never assess feasibility before",
        ),
    },
    "references/backtest-strategy.md": {
        "feasibility follows user selection": (
            "only after the user selects **backtest strategy**",
            "assess feasibility before",
        ),
        "future information is explicit": (
            "must be yes or no before backtest status becomes authorized",
            "cannot demonstrate real-time strategy performance",
        ),
        "methodology and disposition are separate": (
            "methodology describes",
            "disposition separately describes",
        ),
        "runs retain recoverable evidence": (
            "immutable snapshot",
            "exact durable commit",
            "until explicit deletion",
        ),
        "visual evidence is planned and shown": (
            "two to four data-derived visuals",
            "embed saved images",
            "detailed report link alone is not a substitute",
        ),
        "visual failure preserves valid evidence": (
            "one safe mechanical rendering repair",
            "does not by itself make trustworthy evidence failed",
            "same outputs",
        ),
        "revisions supersede without deletion": (
            "mark affected valid evidence superseded",
            "return highest completed outcome to strategy defined",
        ),
    },
    "references/implement-and-activate.md": {
        "missing credentials follow safe storage": (
            "do not request `alphainsider_api_key` before storage",
            "first user-facing implementation action",
            "creation state in progress",
        ),
        "credential values are non-echoing": (
            "protected standard input",
            "never echo",
            "never open `.env`",
        ),
        "strategy choice is exact": (
            "never display a complete api response",
            "select the first result automatically",
            "strict strategy type",
        ),
        "creation ambiguity prevents retry": (
            "ambiguous outcome",
            "do not retry",
            "exactly one new owned match",
        ),
        "verification cannot trade": (
            "tests must not submit or cancel",
            "mock every external service",
        ),
        "notification setup never sends": (
            "never send a setup or test message",
            "user-selected, unverified",
            "notification delivery is not an activation gate",
        ),
        "activation has complete gates": (
            "only after",
            "native scheduler is active for the next scheduled run",
            "asks for no approval",
        ),
        "native task locates the persistent project": (
            "stable persistent project identity",
            "open the persistent project",
        ),
    },
    "references/run-and-recover.md": {
        "dry runs are explicit and isolated": (
            "only an explicit chat request",
            "must not submit, change, or cancel orders",
            "isolated report",
        ),
        "lock replacement requires proof": (
            "never remove a leftover lock",
            "record that evidence",
        ),
        "performance is not health": (
            "profit, loss, return, win rate",
            "are not health criteria",
        ),
        "errors retain active automation": (
            "keep automation state active",
            "operational health degraded/retrying",
            "next trigger",
        ),
        "ambiguous orders gate later work": (
            "never assume success or failure",
            "submit nothing while ambiguity remains",
        ),
        "recovery never replays an order": (
            "never replay a missed signal or order",
            "no strategy or order retry in that trigger",
        ),
        "repairs require progress or new evidence": (
            "no meaningful progress remains",
            "new evidence",
            "never repeat the same failed repair",
        ),
        "notification failures are isolated": (
            "treat channels independently",
            "never pauses trading",
            "without queuing or resending",
        ),
    },
    "references/update-strategy.md": {
        "pending changes preserve confirmed plan": (
            "preserve active confirmed `plan.md`",
            "`pending-update.md`",
            "remains draft",
        ),
        "behavior changes pause safely": (
            "new orders are paused",
            "pause future native automation",
            "shared run or repair lock",
        ),
        "affected evidence is retained": (
            "mark every affected valid run superseded",
            "preserve its methodology",
            "never delete evidence",
        ),
        "performance cannot change behavior": (
            "performance alone never starts",
            "user reviews and confirms",
        ),
        "user edits are detected before writes": (
            "before writing project files or external state",
            "detect user edits",
        ),
        "implementation repairs stay in confirmed scope": (
            "compatible implementation improvements only within",
            "confirmed implementation scope",
        ),
    },
    "references/delete-strategy.md": {
        "deletion requires explicit intent": (
            "only after the user clearly asks",
            "never imply deletion authority",
        ),
        "deletion cannot trade": (
            "never cancels an order",
            "liquidates a position",
            "submits a trade",
        ),
        "full deletion leaves no tombstone": (
            "remove the entire exact selected project",
            "leave no tombstone",
        ),
    },
}

REQUIRED_CORE_LAYOUT = {
    "plan.md",
    ".env.example",
    ".gitignore",
    "README.md",
    "AGENTS.md",
    "strategy/",
    "backtest/",
    "runtime/",
    "tests/",
}
EXPECTED_SETUP_OPERATIONS = {
    "/verifyToken",
    "/getUserInfo",
    "/getStrategies",
    "/getUserStrategies",
    "/newStrategy",
    "/updateStrategy",
    "/deleteStrategy",
    "/getStrategySubscriptions",
    "/getAccountSubscription",
    "/getPositions",
    "/getOrders",
    "/getStocks",
    "/searchStocks",
    "/getExchangeStatus",
}
REQUIRED_NEW_STRATEGY_SETUP_FIELDS = {
    "type",
    "name",
    "input_value",
    "private",
}
REQUIRED_ALPHA_CREDENTIAL_GUIDANCE = {
    "never return the API key or arbitrary environment contents",
    "not secrets like the API key",
    "Never dump the process environment or complete `.env`",
    "prevents accidental output exposure, not hostile same-process inspection",
}
REQUIRED_ALPHA_ROUTING_GUIDANCE = {
    "follow its link to the exact endpoint or WebSocket message section",
    "Do not load unrelated endpoint sections from the same grouped reference",
    "references/api-reference.md` for exact section links",
}
REQUIRED_ALPHA_STREAM_GUIDANCE = {
    "pass `reconnect=True` to `stream_events(...)`",
    "re-subscribes to the complete channel list",
    "authentication failures remain terminal",
}
REQUIRED_ALPHA_DOC_AUDIT_GUIDANCE = {
    "Before finalizing any change under `skills/alphainsider-api/`",
    "https://api.alphainsider.com/llms.txt",
    "https://api.alphainsider.com/openapi.yaml",
    "https://api.alphainsider.com/asyncapi.yaml",
    "Reconcile every discrepancy in the same change",
}
REQUIRED_ALPHA_EXECUTION_BEHAVIORS = {
    "SKILL.md": {
        "focused prose can be stricter than schema": (
            r"\bfocused prose states a stricter compatible rule\b.{0,120}"
            r"\bfollow the prose\b.{0,100}\brecord the documentation discrepancy\b"
        ),
        "exchange status is not order permission": (
            r"\bDo not infer that an exchange-status value permits an order\b"
            r".{0,220}\bdoes not map stock statuses to accepted order sessions\b"
        ),
        "tier limit remains operation scoped": (
            r"\bnew_order\b.{0,100}\bsuccessful direct `/newOrder` requests\b"
            r".{0,160}\bdo not silently apply it to allocation or webhook\b"
        ),
    },
    "references/api-reference.md": {
        "exchange example is not an eligibility rule": (
            r"\bexample value `extended-hours`.{0,100}"
            r"\bpossible response value only\b.{0,300}"
            r"\bkeep stock-session eligibility unresolved\b"
        ),
    },
    "references/stocks.md": {
        "status strings require an explicit mapping": (
            r"\bdo not treat a status string by itself as permission\b"
            r".{0,240}\bdoes not enumerate\b.{0,320}"
            r"\bstock-session eligibility remains unresolved\b"
        ),
    },
    "references/trades.md": {
        "newOrder prose overrides looser schema": (
            r"\bfocused operation prose is stricter than the OpenAPI request schema\b"
            r".{0,180}\bFollow the focused requirement\b"
        ),
        "allocation behavior is materially distinct": (
            r"\bnewOrderAllocations\b.{0,100}\bcomplete desired position set\b"
            r".{0,140}\bcancels existing open orders\b.{0,100}"
            r"\bcloses omitted positions\b"
        ),
        "allocation contract contradictions are recorded": (
            r"\boperation description and response example\b.{0,120}"
            r"\bmarket\b.{0,120}\bslippage\b.{0,100}\blimit order\b"
            r".{0,180}\bprovider `polygon`.{0,120}\benum omits it\b"
        ),
    },
    "references/limits.md": {
        "newOrder tier scope is not generalized": (
            r"\bnew_order\b.{0,120}\bsuccessful direct\b.{0,60}`/newOrder`"
            r".{0,260}\bdoes not state\b.{0,180}"
            r"`/newOrderAllocations` or `/newOrderWebhook`"
        ),
    },
    "references/websockets.md": {
        "example-only WebSocket fields are qualified": (
            r"\bAsyncAPI server-message schemas\b.{0,180}"
            r"\bexamples contain the detailed response objects\b.{0,160}"
            r"\bexample-only fields as illustrative\b"
        ),
    },
}
README_MAX_WORDS = 500
REQUIRED_README_SECTIONS = {
    "# AlphaInsider Skills",
    "## Overview",
    "## Skills",
    "## Install",
    "## How it works",
    "## Development",
}
REQUIRED_README_OVERVIEW_GUIDANCE = {
    "`alphainsider`",
    "`alphainsider-api`",
    "`alphainsider-strategy-creator`",
    "/alphainsider",
    "use the alphainsider skill",
    "npx skills@latest add",
    "root `plan.md`",
    "native AI scheduler",
    "AlphaInsider strategy",
    "fixed code",
    "simulated funds",
    "backtest",
    "self-healing",
    "Explicit deletion",
    "resources#automating-trades",
}
REQUIRED_README_OVERVIEW_BEHAVIORS = {
    "errors-only notifications are the default": (
        r"(?:\bErrors only\b.{0,80}\bdefault\b|"
        r"\bdefault\b.{0,80}\bErrors only\b)"
    ),
    "strategy creation journey is ordered": (
        r"\bDefine Strategy\b.{0,100}\bBacktest Strategy\b.{0,100}"
        r"\bImplement Strategy on AlphaInsider\b"
    ),
    "backtesting is always offered before feasibility": (
        r"\bBacktesting is always offered\b.{0,120}"
        r"\bFeasibility is assessed only after\b"
    ),
    "Complete requires active automation": (
        r"\bCreation is Complete only after\b.{0,160}"
        r"\bnative automation is active\b"
    ),
    "setup sends no test notifications": (
        r"\bSetup discovers notification support without sending test messages\b"
    ),
    "backtest runs preserve disposition and source": (
        r"\bEvery run is a backtest\b.{0,180}\bValid\b.{0,80}\bSuperseded\b"
        r".{0,80}\bFailed\b.{0,100}\brecoverable source\b"
    ),
    "backtests disclose future information": (
        r"\bEvery run is a backtest\b.{0,100}\bfuture-information use\b"
        r".{0,260}\bwarned before results\b.{0,100}\baffected measurements\b"
    ),
    "Define uses actual scheduler and public constraints": (
        r"\bDuring Define\b.{0,120}\bactual native AI scheduler\b"
        r".{0,120}\bpublic AlphaInsider constraints\b"
    ),
    "faster cadence is not simulated": (
        r"\bnever fakes a faster cadence\b.{0,100}\bbackground loop\b"
    ),
    "Define uses explicit sessions then a stock fallback": (
        r"\bExplicit session guidance takes priority\b.{0,180}"
        r"\bstocks use the Strategy Creator fallback\b.{0,100}"
        r"\bcryptocurrency is available 24/7\b"
    ),
    "operational errors retry without pausing automation": (
        r"\brun error ends that run's order work\b.{0,140}"
        r"\bautomation stays Active\b.{0,100}\bDegraded/Retrying\b"
        r".{0,100}\bnext trigger\b"
    ),
    "only current Valid evidence advances": (
        r"\bOnly Valid evidence for the current strategy advances\b"
    ),
    "notification repair needs enabled confirmed scope": (
        r"\bNotification repair\b.{0,120}"
        r"\benabled, confirmed self-healing scope\b"
    ),
    "backtest summaries include result visuals": (
        r"\bFindings summaries embed or directly link\b.{0,60}"
        r"\btwo to four saved data-derived visuals\b.{0,80}"
        r"\bdetailed report alone is insufficient\b"
    ),
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"{path}: invalid frontmatter line {line!r}")
        fields[key.strip()] = value.strip()
    return fields


def markdown_anchor(heading: str) -> str:
    """Return the anchor used by the grouped AlphaInsider references."""
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def section_link(label: str, reference: str, heading: str) -> str:
    return f"[`{label}`]({reference}#{markdown_anchor(heading)})"


def local_link_targets(
    source: Path, text: str, root: Path
) -> tuple[set[Path], set[str]]:
    """Return valid in-root links and invalid local targets from Markdown."""
    targets: set[Path] = set()
    invalid: set[str] = set()
    resolved_root = root.resolve()

    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        raw_target = match.group(1).strip("<>")
        path_text = raw_target.split("#", 1)[0]
        if not path_text:
            continue
        if URI_SCHEME_PATTERN.match(path_text):
            continue
        if path_text.startswith("/"):
            invalid.add(raw_target)
            continue

        target = (source.parent / path_text).resolve()
        try:
            target.relative_to(resolved_root)
        except ValueError:
            invalid.add(raw_target)
            continue
        if not target.is_file():
            invalid.add(raw_target)
            continue
        targets.add(target)

    return targets, invalid


def ordered_list_sequence_errors(text: str) -> list[str]:
    """Return malformed explicit ordered-list items outside fenced code."""
    errors: list[str] = []
    next_number_by_indent: dict[int, int] = {}
    fence_marker: str | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence:
            marker = fence.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue
        if fence_marker is not None or not stripped:
            continue

        item = re.match(r"^( *)(\d+)\. ", line)
        if item:
            indent = len(item.group(1))
            number = int(item.group(2))
            expected = next_number_by_indent.get(indent, 1)
            if number != expected:
                errors.append(
                    f"line {line_number} uses {number}; expected {expected} "
                    f"at indentation {indent}"
                )
            next_number_by_indent[indent] = number + 1
            next_number_by_indent = {
                depth: value
                for depth, value in next_number_by_indent.items()
                if depth <= indent
            }
            continue

        if stripped.startswith("#"):
            next_number_by_indent.clear()
            continue

        indent = len(line) - len(stripped)
        next_number_by_indent = {
            depth: value
            for depth, value in next_number_by_indent.items()
            if depth < indent
        }

    return errors


def catalog_specialists(text: str) -> list[str]:
    """Return routable specialist names from catalog headings."""
    return CATALOG_HEADING_PATTERN.findall(text)


def literal_string_collection(
    tree: ast.Module, assignment_name: str
) -> set[str] | None:
    """Read a literal string collection from a module assignment."""
    value_node: ast.expr | None = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == assignment_name
            for target in node.targets
        ):
            value_node = node.value
            break
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == assignment_name
        ):
            value_node = node.value
            break
    if value_node is None:
        return None
    if (
        isinstance(value_node, ast.Call)
        and isinstance(value_node.func, ast.Name)
        and value_node.func.id == "frozenset"
        and len(value_node.args) == 1
        and not value_node.keywords
    ):
        value_node = value_node.args[0]
    try:
        values = ast.literal_eval(value_node)
    except (TypeError, ValueError):
        return None
    if not isinstance(values, (set, frozenset, list, tuple)) or not all(
        isinstance(value, str) for value in values
    ):
        return None
    return set(values)


def function_calls(tree: ast.Module, function_name: str, called_name: str) -> bool:
    """Return whether one module function calls a named function."""
    function = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == function_name
        ),
        None,
    )
    return function is not None and any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == called_name
        for node in ast.walk(function)
    )


def validate() -> list[str]:
    errors: list[str] = []
    agent_guide_text = " ".join(
        (ROOT / "AGENTS.md").read_text(encoding="utf-8").split()
    )
    discovered = {path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md")}
    if discovered != EXPECTED_SKILLS:
        errors.append(
            f"expected skills {sorted(EXPECTED_SKILLS)}, found {sorted(discovered)}"
        )

    all_skill_files = list(SKILLS_DIR.glob("*/SKILL.md"))
    if len(all_skill_files) != len(EXPECTED_SKILLS):
        errors.append(
            f"expected exactly {len(EXPECTED_SKILLS)} SKILL.md files, "
            f"found {len(all_skill_files)}"
        )

    for name in sorted(EXPECTED_SKILLS):
        skill_dir = SKILLS_DIR / name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        try:
            fields = frontmatter(skill_md)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if set(fields) != {"name", "description"}:
            errors.append(f"{name}: frontmatter must contain only name and description")
        if fields.get("name") != name:
            errors.append(f"{name}: frontmatter name does not match directory")
        if len(fields.get("description", "")) < 40:
            errors.append(f"{name}: description is too short")

    wrapper = SKILLS_DIR / WRAPPER_NAME
    wrapper_skill = wrapper / "SKILL.md"
    wrapper_references = wrapper / "references"
    wrapper_scripts = wrapper / "scripts"
    if wrapper_skill.is_file():
        wrapper_text = wrapper_skill.read_text(encoding="utf-8")
        wrapper_fields = frontmatter(wrapper_skill)
        missing_wrapper_triggers = {
            trigger
            for trigger in REQUIRED_WRAPPER_TRIGGERS
            if trigger not in wrapper_fields.get("description", "")
        }
        if missing_wrapper_triggers:
            errors.append(
                "alphainsider description is missing explicit invoke triggers "
                f"{sorted(missing_wrapper_triggers)}"
            )
        missing_wrapper_guidance = {
            guidance
            for guidance in REQUIRED_WRAPPER_GUIDANCE
            if guidance not in wrapper_text
        }
        if missing_wrapper_guidance:
            errors.append(
                "alphainsider is missing facade guidance "
                f"{sorted(missing_wrapper_guidance)}"
            )

    actual_wrapper_refs = {
        path.name
        for path in wrapper_references.iterdir()
        if path.is_file()
    } if wrapper_references.is_dir() else set()
    if actual_wrapper_refs != EXPECTED_WRAPPER_REFERENCES:
        errors.append(
            "alphainsider references must be exactly "
            f"{sorted(EXPECTED_WRAPPER_REFERENCES)}"
        )
    if wrapper_references.is_dir():
        extra_wrapper_dirs = {
            path.name for path in wrapper_references.iterdir() if path.is_dir()
        }
        if extra_wrapper_dirs:
            errors.append(
                "alphainsider references must not contain nested directories "
                f"{sorted(extra_wrapper_dirs)}"
            )

    actual_wrapper_scripts = {
        path.relative_to(wrapper_scripts).as_posix()
        for path in wrapper_scripts.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    } if wrapper_scripts.is_dir() else set()
    if actual_wrapper_scripts != EXPECTED_WRAPPER_SCRIPTS:
        errors.append(
            "alphainsider scripts must be exactly "
            f"{sorted(EXPECTED_WRAPPER_SCRIPTS)}"
        )

    catalog_path = wrapper_references / "catalog.md"
    catalog_names: list[str] = []
    if catalog_path.is_file():
        catalog_text = catalog_path.read_text(encoding="utf-8")
        catalog_names = catalog_specialists(catalog_text)
        catalog_set = set(catalog_names)
        if WRAPPER_NAME in catalog_set:
            errors.append("alphainsider catalog must not list itself")
        if len(catalog_names) != len(catalog_set):
            errors.append("alphainsider catalog headings must be unique")
        if catalog_set | {WRAPPER_NAME} != EXPECTED_SKILLS:
            errors.append(
                "alphainsider catalog must list every specialist skill exactly "
                f"once: expected {sorted(EXPECTED_SKILLS - {WRAPPER_NAME})}, "
                f"found {sorted(catalog_set)}"
            )
        for name in catalog_names:
            if not (SKILLS_DIR / name / "SKILL.md").is_file():
                errors.append(
                    f"alphainsider catalog lists {name} without skills/{name}/SKILL.md"
                )
            if f"--skill {name}" not in catalog_text:
                errors.append(
                    f"alphainsider catalog must include the {name} install command"
                )
        if catalog_names != sorted(catalog_names):
            errors.append(
                "alphainsider catalog headings must be in ascending name order"
            )

    strategy = SKILLS_DIR / "alphainsider-strategy-creator"
    strategy_references = strategy / "references"
    actual_strategy_refs = {
        path.name for path in strategy_references.iterdir() if path.is_file()
    }
    if actual_strategy_refs != EXPECTED_STRATEGY_REFERENCES:
        errors.append(
            "strategy-creator references must be exactly "
            f"{sorted(EXPECTED_STRATEGY_REFERENCES)}"
        )
    nested_strategy_reference_dirs = {
        path.name for path in strategy_references.iterdir() if path.is_dir()
    }
    if nested_strategy_reference_dirs:
        errors.append(
            "strategy-creator references must not contain nested directories "
            f"{sorted(nested_strategy_reference_dirs)}"
        )

    strategy_scripts_dir = strategy / "scripts"
    strategy_scripts = {
        path.relative_to(strategy_scripts_dir).as_posix()
        for path in strategy_scripts_dir.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if strategy_scripts != EXPECTED_STRATEGY_SCRIPTS:
        errors.append(
            "strategy-creator scripts must be exactly "
            f"{sorted(EXPECTED_STRATEGY_SCRIPTS)}"
        )

    strategy_text = (strategy / "SKILL.md").read_text(encoding="utf-8")
    reference_texts = {
        name: (strategy_references / name).read_text(encoding="utf-8")
        for name in EXPECTED_STRATEGY_REFERENCES
    }
    all_reference_text = "\n".join(
        reference_texts[name] for name in sorted(reference_texts)
    )

    if len(strategy_text.split()) > STRATEGY_SKILL_MAX_WORDS:
        errors.append(
            "strategy-creator SKILL.md exceeds compact-word limit "
            f"{STRATEGY_SKILL_MAX_WORDS}"
        )

    strategy_sources = {"SKILL.md": strategy / "SKILL.md"}
    strategy_sources.update(
        {
            f"references/{name}": strategy_references / name
            for name in EXPECTED_STRATEGY_REFERENCES
        }
    )
    strategy_source_texts = {"SKILL.md": strategy_text}
    strategy_source_texts.update(
        {
            f"references/{name}": text_value
            for name, text_value in reference_texts.items()
        }
    )
    reference_graph: dict[str, set[str]] = {}
    broken_strategy_links: set[str] = set()
    for source_name, source_path in strategy_sources.items():
        targets, invalid = local_link_targets(
            source_path, strategy_source_texts[source_name], strategy
        )
        routed_targets = {
            target.relative_to(strategy).as_posix() for target in targets
        }
        reference_graph[source_name] = routed_targets & set(strategy_sources)
        broken_strategy_links.update(
            f"{source_name} -> {target}" for target in invalid
        )

    if broken_strategy_links:
        errors.append(
            "strategy-creator has invalid local links "
            f"{sorted(broken_strategy_links)}"
        )

    reachable_strategy_files = {"SKILL.md"}
    frontier = ["SKILL.md"]
    while frontier:
        source_name = frontier.pop()
        for target_name in reference_graph.get(source_name, set()):
            if target_name not in reachable_strategy_files:
                reachable_strategy_files.add(target_name)
                frontier.append(target_name)

    missing_reference_routes = {
        name
        for name in EXPECTED_STRATEGY_REFERENCES
        if f"references/{name}" not in reachable_strategy_files
    }
    if missing_reference_routes:
        errors.append(
            "strategy-creator references are not reachable from SKILL.md "
            f"{sorted(missing_reference_routes)}"
        )

    for source_name, required_targets in REQUIRED_STRATEGY_LINKS.items():
        missing_targets = required_targets - reference_graph.get(source_name, set())
        if missing_targets:
            errors.append(
                f"strategy-creator {source_name} is missing workflow routes "
                f"{sorted(missing_targets)}"
            )

    expected_outline_owners = {"SKILL.md"} | {
        f"references/{name}" for name in EXPECTED_STRATEGY_REFERENCES
    }
    actual_outline_owners = set(REQUIRED_STRATEGY_OUTLINE_HEADINGS)
    if actual_outline_owners != expected_outline_owners:
        errors.append(
            "strategy-creator outline validation must cover every instruction "
            f"file exactly once: expected {sorted(expected_outline_owners)}, "
            f"found {sorted(actual_outline_owners)}"
        )

    for owner, expected_headings in REQUIRED_STRATEGY_OUTLINE_HEADINGS.items():
        actual_headings = tuple(
            line
            for line in strategy_source_texts[owner].splitlines()
            if re.match(r"^#{2,6} ", line)
        )
        if actual_headings != expected_headings:
            errors.append(
                f"strategy-creator {owner} must keep its ranked workflow "
                f"hierarchy in order {list(expected_headings)}"
            )

        heading_levels = [
            len(line) - len(line.lstrip("#")) for line in actual_headings
        ]
        if heading_levels and (
            heading_levels[0] != 2
            or any(
                child > parent + 1
                for parent, child in zip(
                    heading_levels, heading_levels[1:]
                )
            )
        ):
            errors.append(
                f"strategy-creator {owner} has a skipped heading level"
            )

        sequence_errors = ordered_list_sequence_errors(
            strategy_source_texts[owner]
        )
        if sequence_errors:
            errors.append(
                f"strategy-creator {owner} has malformed ordered workflow "
                f"lists {sequence_errors}"
            )

    for owner, literals in REQUIRED_STRATEGY_LITERALS.items():
        owner_text = " ".join(strategy_source_texts[owner].split())
        missing_literals = {
            item for item in literals if item not in owner_text
        }
        if missing_literals:
            errors.append(
                f"strategy-creator {owner} is missing stable contract values "
                f"{sorted(missing_literals)}"
            )

    for owner, literals in FORBIDDEN_STRATEGY_LITERALS.items():
        owner_text = " ".join(strategy_source_texts[owner].split())
        present_literals = {item for item in literals if item in owner_text}
        if present_literals:
            errors.append(
                f"strategy-creator {owner} contains obsolete contract values "
                f"{sorted(present_literals)}"
            )

    obsolete_backtest_names = {
        f"{owner}: {name}"
        for owner, owner_text in strategy_source_texts.items()
        for name, pattern in FORBIDDEN_BACKTEST_NAME_PATTERNS.items()
        if pattern.search(owner_text)
    }
    if obsolete_backtest_names:
        errors.append(
            "strategy-creator contains obsolete backtest names "
            f"{sorted(obsolete_backtest_names)}"
        )

    for owner, concepts in REQUIRED_STRATEGY_CONCEPTS.items():
        owner_text = " ".join(strategy_source_texts[owner].split()).casefold()
        missing_concepts = {
            name: tuple(
                fragment
                for fragment in fragments
                if fragment.casefold() not in owner_text
            )
            for name, fragments in concepts.items()
        }
        missing_concepts = {
            name: fragments
            for name, fragments in missing_concepts.items()
            if fragments
        }
        if missing_concepts:
            errors.append(
                f"strategy-creator {owner} is missing semantic contracts "
                f"{missing_concepts}"
            )

    plan_template = strategy_references / "plan-template.md"
    plan_text = reference_texts["plan-template.md"]
    if plan_text.startswith("---"):
        errors.append("strategy plan template must not use lifecycle frontmatter")

    plan_headings = tuple(
        line
        for line in plan_text.splitlines()
        if line in set(REQUIRED_PLAN_SECTION_ORDER)
    )
    if plan_headings != REQUIRED_PLAN_SECTION_ORDER:
        errors.append(
            "strategy plan template sections must use order "
            f"{list(REQUIRED_PLAN_SECTION_ORDER)}"
        )

    plan_field_lines = tuple(
        line
        for line in plan_text.splitlines()
        if re.match(r"^- [^:]+:", line)
    )
    if len(REQUIRED_PLAN_FIELD_LINES) != 77:
        errors.append(
            "strategy plan validator must define exactly 77 field-line "
            "contracts"
        )
    if plan_field_lines != REQUIRED_PLAN_FIELD_LINES:
        mismatch_index = next(
            (
                index
                for index, (actual, expected) in enumerate(
                    zip(plan_field_lines, REQUIRED_PLAN_FIELD_LINES), start=1
                )
                if actual != expected
            ),
            min(len(plan_field_lines), len(REQUIRED_PLAN_FIELD_LINES)) + 1,
        )
        actual_line = (
            plan_field_lines[mismatch_index - 1]
            if mismatch_index <= len(plan_field_lines)
            else "<missing>"
        )
        expected_line = (
            REQUIRED_PLAN_FIELD_LINES[mismatch_index - 1]
            if mismatch_index <= len(REQUIRED_PLAN_FIELD_LINES)
            else "<none>"
        )
        errors.append(
            "strategy plan template must preserve all 77 field labels, "
            "defaults, inline enums, comments, and field order; first mismatch "
            f"at field {mismatch_index}: expected {expected_line!r}, "
            f"found {actual_line!r}"
        )

    strategy_id_field_references = {
        name
        for name, text_value in reference_texts.items()
        if "\n- AlphaInsider strategy ID:" in text_value
    }
    if strategy_id_field_references != {"plan-template.md"}:
        errors.append(
            "only plan-template.md may define the AlphaInsider strategy ID field"
        )

    project_contract_text = reference_texts["project-contract.md"]
    missing_layout_entries = {
        entry for entry in REQUIRED_CORE_LAYOUT if entry not in project_contract_text
    }
    if missing_layout_entries:
        errors.append(
            "strategy project contract is missing core layout entries "
            f"{sorted(missing_layout_entries)}"
        )

    lifecycle_frontmatter = re.findall(
        r"^status:\s*(draft|confirmed|implemented|retired)\s*$",
        all_reference_text,
        re.MULTILINE,
    )
    if lifecycle_frontmatter:
        errors.append(
            "strategy references must not define legacy lifecycle status "
            f"{sorted(set(lifecycle_frontmatter))}"
        )

    env_helper = strategy_scripts_dir / "set_env_value.py"
    if env_helper.is_file():
        helper_source = env_helper.read_text(encoding="utf-8")
        required_helper_markers = {
            'if __name__ != "__main__":',
            "set_env_value.py is CLI-only",
            '"--project-root",',
            '"--remove",',
            "getpass.getpass",
            "sys.stdin.buffer.read",
            '_validate_project_root(chosen_root)',
            'resolved_root / "plan.md"',
            "env_path.is_symlink()",
            "os.replace(",
            "0o600",
            "_MAX_VALUE_BYTES",
            "_MAX_ENV_BYTES",
        }
        missing_helper_markers = {
            item for item in required_helper_markers if item not in helper_source
        }
        if missing_helper_markers:
            errors.append(
                "strategy environment helper is missing safeguards "
                f"{sorted(missing_helper_markers)}"
            )
        forbidden_helper_markers = {
            'parser.add_argument("value"',
            'resolved_root / "docs"',
        }
        present_forbidden_helper_markers = {
            item for item in forbidden_helper_markers if item in helper_source
        }
        if present_forbidden_helper_markers:
            errors.append(
                "strategy environment helper contains obsolete input or plan paths "
                f"{sorted(present_forbidden_helper_markers)}"
            )
        public_helper_functions = re.findall(
            r"^def ([A-Za-z][A-Za-z0-9_]*)\(", helper_source, re.MULTILINE
        )
        if public_helper_functions:
            errors.append(
                "strategy environment helper exposes public Python functions "
                f"{sorted(public_helper_functions)}"
            )

    setup_wrapper = strategy_scripts_dir / "alphainsider_setup_request.py"
    if setup_wrapper.is_file():
        wrapper_source = setup_wrapper.read_text(encoding="utf-8")
        required_wrapper_markers = {
            'if __name__ != "__main__":',
            "alphainsider_setup_request.py is CLI-only",
            '"--project-root",',
            "--print-config",
            "--json-stdin",
            'resolved_root / "plan.md"',
            "_NoRedirectHandler",
            "_ALLOWED_OPERATIONS",
            "MAX_RESPONSE_BYTES",
            "MAX_REQUEST_BODY_BYTES",
            "MAX_ENV_BYTES",
            "_validated_api_key",
            "_credential_values",
            "path.is_symlink()",
        }
        missing_wrapper_markers = {
            item for item in required_wrapper_markers if item not in wrapper_source
        }
        if missing_wrapper_markers:
            errors.append(
                "strategy setup wrapper is missing safeguards "
                f"{sorted(missing_wrapper_markers)}"
            )

        operation_block = re.search(
            r"_ALLOWED_OPERATIONS = \{(.*?)\n\}",
            wrapper_source,
            re.DOTALL,
        )
        setup_operations = (
            set(re.findall(r'"(/[^"]+)":', operation_block.group(1)))
            if operation_block
            else set()
        )
        if setup_operations != EXPECTED_SETUP_OPERATIONS:
            errors.append(
                "strategy setup wrapper operation allowlist must be exactly "
                f"{sorted(EXPECTED_SETUP_OPERATIONS)}"
            )

        try:
            wrapper_tree = ast.parse(wrapper_source)
        except SyntaxError:
            wrapper_tree = None

        new_strategy_fields = (
            literal_string_collection(
                wrapper_tree, "_NEW_STRATEGY_REQUIRED_FIELDS"
            )
            if wrapper_tree is not None
            else None
        )
        if new_strategy_fields != REQUIRED_NEW_STRATEGY_SETUP_FIELDS:
            errors.append(
                "strategy setup wrapper newStrategy fields must be exactly "
                f"{sorted(REQUIRED_NEW_STRATEGY_SETUP_FIELDS)}"
            )

        guard_is_called = wrapper_tree is not None and function_calls(
            wrapper_tree, "_build_request", "_validate_setup_body"
        )
        if not guard_is_called:
            errors.append(
                "strategy setup wrapper must enforce its newStrategy body guard"
            )

        forbidden_wrapper_markers = {
            '"--base-url"',
            "urllib.request.urlopen(",
            'resolved_root / "docs"',
            '"/newOrder"',
            '"/newOrderAllocations"',
            '"/deleteOrder"',
        }
        present_forbidden_wrapper_markers = {
            item for item in forbidden_wrapper_markers if item in wrapper_source
        }
        if present_forbidden_wrapper_markers:
            errors.append(
                "strategy setup wrapper exposes unsafe or obsolete behavior "
                f"{sorted(present_forbidden_wrapper_markers)}"
            )
        public_wrapper_functions = re.findall(
            r"^def ([A-Za-z][A-Za-z0-9_]*)\(", wrapper_source, re.MULTILINE
        )
        if public_wrapper_functions:
            errors.append(
                "strategy setup wrapper exposes public Python functions "
                f"{sorted(public_wrapper_functions)}"
            )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme_text.split())
    obsolete_readme_backtest_names = {
        name
        for name, pattern in FORBIDDEN_BACKTEST_NAME_PATTERNS.items()
        if pattern.search(normalized_readme)
    }
    if obsolete_readme_backtest_names:
        errors.append(
            "README contains obsolete backtest names "
            f"{sorted(obsolete_readme_backtest_names)}"
        )
    missing_readme_sections = REQUIRED_README_SECTIONS - set(
        readme_text.splitlines()
    )
    if missing_readme_sections:
        errors.append(
            "README is missing sections " f"{sorted(missing_readme_sections)}"
        )

    readme_word_count = len(readme_text.split())
    if readme_word_count > README_MAX_WORDS:
        errors.append(
            f"README must not exceed {README_MAX_WORDS} words; "
            f"found {readme_word_count}"
        )

    missing_readme_overview_guidance = {
        guidance
        for guidance in REQUIRED_README_OVERVIEW_GUIDANCE
        if guidance not in normalized_readme
    }
    if missing_readme_overview_guidance:
        errors.append(
            "README is missing high-level guidance "
            f"{sorted(missing_readme_overview_guidance)}"
        )
    missing_readme_overview_behaviors = {
        name
        for name, pattern in REQUIRED_README_OVERVIEW_BEHAVIORS.items()
        if re.search(pattern, normalized_readme, re.IGNORECASE) is None
    }
    if missing_readme_overview_behaviors:
        errors.append(
            "README is missing high-level behavior "
            f"{sorted(missing_readme_overview_behaviors)}"
        )
    readme_install_skills = re.findall(r"--skill ([a-z0-9-]+)", readme_text)
    if not readme_install_skills or readme_install_skills[0] != WRAPPER_NAME:
        errors.append("README must lead with the alphainsider install")

    alphainsider = SKILLS_DIR / "alphainsider-api"
    alphainsider_text = (alphainsider / "SKILL.md").read_text(encoding="utf-8")
    missing_alpha_credential_guidance = {
        guidance
        for guidance in REQUIRED_ALPHA_CREDENTIAL_GUIDANCE
        if guidance not in " ".join(alphainsider_text.split())
    }
    if missing_alpha_credential_guidance:
        errors.append(
            "alphainsider is missing credential boundary guidance "
            f"{sorted(missing_alpha_credential_guidance)}"
        )

    normalized_alphainsider_text = " ".join(alphainsider_text.split())
    missing_alpha_routing_guidance = {
        guidance
        for guidance in REQUIRED_ALPHA_ROUTING_GUIDANCE
        if guidance not in normalized_alphainsider_text
    }
    if missing_alpha_routing_guidance:
        errors.append(
            "alphainsider is missing focused section routing guidance "
            f"{sorted(missing_alpha_routing_guidance)}"
        )

    alpha_execution_sources = {
        "SKILL.md": alphainsider_text,
        **{
            owner: (alphainsider / owner).read_text(encoding="utf-8")
            for owner in REQUIRED_ALPHA_EXECUTION_BEHAVIORS
            if owner != "SKILL.md"
        },
    }
    for owner, behaviors in REQUIRED_ALPHA_EXECUTION_BEHAVIORS.items():
        owner_text = " ".join(alpha_execution_sources[owner].split())
        missing_behaviors = {
            name
            for name, pattern in behaviors.items()
            if re.search(pattern, owner_text, re.IGNORECASE) is None
        }
        if missing_behaviors:
            errors.append(
                f"alphainsider-api {owner} is missing execution contracts "
                f"{sorted(missing_behaviors)}"
            )

    normalized_alpha_execution_text = " ".join(
        "\n".join(alpha_execution_sources.values()).split()
    )
    if re.search(
        r"\bstock orders?\b.{0,120}\b(?:only|must)\b.{0,80}"
        r"\bregular market hours\b",
        normalized_alpha_execution_text,
        re.IGNORECASE,
    ):
        errors.append(
            "alphainsider-api must not assert undocumented regular-hours-only "
            "stock order eligibility"
        )

    websocket_guidance = " ".join(
        (
            alphainsider_text
            + "\n"
            + (alphainsider / "references" / "websockets.md").read_text(
                encoding="utf-8"
            )
        ).split()
    )
    missing_alpha_stream_guidance = {
        guidance
        for guidance in REQUIRED_ALPHA_STREAM_GUIDANCE
        if guidance not in websocket_guidance
    }
    if missing_alpha_stream_guidance:
        errors.append(
            "alphainsider is missing WebSocket recovery guidance "
            f"{sorted(missing_alpha_stream_guidance)}"
        )

    missing_alpha_doc_audit_guidance = {
        guidance
        for guidance in REQUIRED_ALPHA_DOC_AUDIT_GUIDANCE
        if guidance not in agent_guide_text
    }
    if missing_alpha_doc_audit_guidance:
        errors.append(
            "AGENTS.md is missing live AlphaInsider docs audit guidance "
            f"{sorted(missing_alpha_doc_audit_guidance)}"
        )

    alpha_scripts = {
        path.relative_to(alphainsider / "scripts").as_posix()
        for path in (alphainsider / "scripts").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if alpha_scripts != EXPECTED_ALPHA_SCRIPTS:
        errors.append(
            "alphainsider scripts must be exactly "
            f"{sorted(EXPECTED_ALPHA_SCRIPTS)}"
        )

    alpha_references = {
        path.name for path in (alphainsider / "references").glob("*.md")
    }
    if alpha_references != EXPECTED_ALPHA_REFERENCES:
        errors.append(
            "alphainsider references must be exactly "
            f"{sorted(EXPECTED_ALPHA_REFERENCES)}"
        )

    api_reference_text = (
        alphainsider / "references" / "api-reference.md"
    ).read_text(encoding="utf-8")
    actual_rest_sections: list[tuple[str, str, str, str]] = []
    expected_rest_sections: list[tuple[str, str, str, str]] = []
    rest_heading_pattern = re.compile(
        r"^## ([A-Za-z][A-Za-z0-9_]*) - "
        r"(GET|POST|PUT|PATCH|DELETE) `(/[^`]+)`$",
        re.MULTILINE,
    )
    for reference, sections in EXPECTED_ALPHA_REST_SECTIONS.items():
        reference_text = (
            alphainsider / "references" / reference
        ).read_text(encoding="utf-8")
        actual_rest_sections.extend(
            (reference, operation_id, method, path)
            for operation_id, method, path in rest_heading_pattern.findall(
                reference_text
            )
        )
        for operation_id, method, path in sections:
            heading = f"{operation_id} - {method} `{path}`"
            expected_rest_sections.append(
                (reference, operation_id, method, path)
            )
            if reference_text.splitlines().count(f"## {heading}") != 1:
                errors.append(
                    "alphainsider REST section must appear exactly once: "
                    f"{reference} {heading}"
                )
            link = section_link(operation_id, reference, heading)
            if api_reference_text.count(link) != 1:
                errors.append(
                    "alphainsider API map must link exactly once to "
                    f"{reference} section {operation_id}"
                )
            if reference == "bots.md":
                local_link = section_link(operation_id, "", heading)
                if local_link not in reference_text:
                    errors.append(
                        f"{reference} contents must link to {operation_id}"
                    )

    if sorted(actual_rest_sections) != sorted(expected_rest_sections):
        errors.append(
            "alphainsider grouped REST headings do not match the expected "
            "operation inventory"
        )

    websocket_reference = alphainsider / "references" / "websockets.md"
    websocket_text = websocket_reference.read_text(encoding="utf-8")
    websocket_heading_pattern = re.compile(
        r"^## ([A-Za-z][A-Za-z0-9_]*) - (.+)$", re.MULTILINE
    )
    actual_websocket_sections = websocket_heading_pattern.findall(websocket_text)
    if actual_websocket_sections != list(EXPECTED_ALPHA_WEBSOCKET_SECTIONS):
        errors.append(
            "alphainsider WebSocket headings do not match the expected "
            "message inventory"
        )
    for message_name, title in EXPECTED_ALPHA_WEBSOCKET_SECTIONS:
        heading = f"{message_name} - {title}"
        api_link = section_link(message_name, "websockets.md", heading)
        if api_reference_text.count(api_link) != 1:
            errors.append(
                "alphainsider API map must link exactly once to WebSocket "
                f"message {message_name}"
            )
        contents_link = section_link(message_name, "", heading)
        if contents_link not in websocket_text:
            errors.append(
                "websockets.md message contents must link to "
                f"{message_name}"
            )

    helper_markers = {
        "scripts/alphainsider_request.py",
        "scripts/alphainsider_stream.py",
        "stream_events(",
    }
    references_with_helper_guidance = {
        path.name
        for path in (alphainsider / "references").glob("*.md")
        if any(marker in path.read_text(encoding="utf-8") for marker in helper_markers)
    }
    if references_with_helper_guidance:
        errors.append(
            "alphainsider references must contain API information only; "
            "helper guidance found in "
            f"{sorted(references_with_helper_guidance)}"
        )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("validated skills: " + ", ".join(sorted(EXPECTED_SKILLS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
