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
    "alphainsider-strategy.md",
    "automation.md",
    "backtesting.md",
    "changes-and-deletion.md",
    "credentials.md",
    "generated-project.md",
    "implementation.md",
    "interview.md",
    "plan-template.md",
    "project-root.md",
    "scheduled-runs.md",
    "user-communication.md",
}
EXPECTED_STRATEGY_SCRIPTS = {
    "alphainsider_setup_request.py",
    "set_env_value.py",
}
STRATEGY_SKILL_MAX_WORDS = 700
REQUIRED_PLAN_SECTION_ORDER = (
    "# Strategy Plan",
    "## Strategy plan",
    "## Backtesting plan",
    "## AlphaInsider setup plan",
    "## Current status",
)
REQUIRED_PLAN_FIELDS = {
    "- Goal:",
    "- Strategy type:",
    "- Assets this strategy can trade:",
    "- How decisions are made:",
    "- Native scheduler surface, supported timing limits, source, and checked time:",
    "- AlphaInsider public constraints, session policy and source, checked time, and unresolved documentation differences:",
    "- Planned AlphaInsider execution operation and material side effects:",
    "- Maximum strategy exposure and execution-specific limit:",
    "- Known account-tier dependency to verify during implementation:",
    "- Open orders, duplicate prevention, retries, and saved state:",
    "- Strategy schedule, timezone, daylight-saving behavior, and market-hours rules:",
    "- Backtest choice:",
    "- Feasibility finding and recommended approach:",
    "- Uses information unavailable at the historical decision time:",
    "- Differences from intended automated execution and other limitations:",
    "- Backtest period and decision times:",
    "- Comparison investment (benchmark):",
    "- Results to show and charts:",
    "- Checks that the backtest follows the strategy plan:",
    "- Backtest run history, changes, future-information use, limitations, dispositions, source snapshots, and artifact paths:",
    "- Featured Valid result for the current strategy:",
    "- Scheduled strategy-run design:",
    "- Strategy run and AI decision flow:",
    "- Create a new or use an existing AlphaInsider strategy:",
    "- Existing AlphaInsider strategy reuse confirmation:",
    "- AlphaInsider strategy name:",
    "- AlphaInsider simulated starting value:",
    "- AlphaInsider public or private setting:",
    "- AlphaInsider paid access and access price:",
    "- AlphaInsider strategy ID:",
    "- AlphaInsider strategy URL:",
    "- AlphaInsider strategy description:",
    "- Native AI scheduler and scheduled task name:",
    "- Schedule frequency, timezone, daylight-saving behavior, and missed runs:",
    "- One-run-at-a-time, Run now, chat run, and chat dry run behavior:",
    "- Operational error retry, reconciliation, and duplicate-notification behavior:",
    "- Self-healing:",
    "- What automatic repair can change, whether notification repair is in scope, what it must protect, how it undoes a failed repair, and time limit:",
    "- Notifications:",
    "- AlphaInsider API access needed for setup and strategy runs:",
    "- Notification events, channels, and safe destination references:",
    "- Notification support status for each selected channel:",
    "- Future authority for AlphaInsider paper orders that follow this plan:",
    "- Creation state:",
    "- Phase:",
    "- Strategy status:",
    "- Backtest status:",
    "- AlphaInsider setup status:",
    "- Highest completed outcome:",
    "- Automation state:",
    "- Automation state reason:",
    "- Operational health:",
    "- Operational health detail and next retry:",
    "- Creation state reason:",
    "- Last completed step:",
    "- Next step:",
    "- Waiting for:",
    "- Open questions:",
    "- Last updated:",
}
REQUIRED_PLAN_ENUMS = {
    "- Creation state:": (
        "In progress",
        "Stopped",
        "Blocked",
        "Complete",
    ),
    "- Phase:": (
        "Defining strategy",
        "Assessing backtest",
        "Planning backtest",
        "Building backtest",
        "Reviewing results",
        "Planning implementation",
        "Building implementation",
        "Configuring automation",
        "Complete",
    ),
    "- Strategy status:": ("Draft", "Confirmed"),
    "- Backtest status:": (
        "Not started",
        "Draft",
        "Authorized",
        "Completed",
        "Failed",
        "Skipped",
    ),
    "- AlphaInsider setup status:": (
        "Not started",
        "Draft",
        "Authorized",
        "Active",
    ),
    "- Highest completed outcome:": (
        "None",
        "Strategy defined",
        "Backtest",
        "Automated strategy",
    ),
    "- Automation state:": ("Not configured", "Active", "Paused"),
    "- Operational health:": (
        "Not active",
        "Ready",
        "Healthy",
        "Degraded/Retrying",
    ),
}
REQUIRED_PLAN_COMMENT_ENUMS = {
    "- Backtest choice:": ("Not asked", "Selected", "Skipped"),
    "- Uses information unavailable at the historical decision time:": (
        "Not assessed",
        "Yes",
        "No",
    ),
    "- Notification events, channels, and safe destination references:": (
        "errors only (recommended)",
        "errors and completed repairs",
        "errors, completed repairs, and warnings",
    ),
    "- Notification support status for each selected channel:": (
        "supported",
        "user-selected, unverified",
    ),
}
REQUIRED_INTERVIEW_PHASE_ORDER = (
    "## Stage 1: Define Strategy",
    "## Stage 2: Backtest Strategy",
    "## Stage 3: Implement Strategy on AlphaInsider",
    "## Completion",
)
REQUIRED_ALPHA_SETUP_SECTION_ORDER = (
    "### Access gate",
    "### AlphaInsider strategy choice",
    "### Implementation and automation choices",
    "### Review AlphaInsider setup and choose the next step",
)
# Stable user-facing labels, paths, limits, and links are intentional literals.
# Behavioral rules use flexible patterns below so validation does not freeze
# incidental sentence wording.
REQUIRED_STRATEGY_LITERALS = {
    "references/user-communication.md": {
        "ASD-STE100-style technical English",
        "👉 **Action — Short title:**",
        "💡 **Optional next step — Short title:**",
        "`⚠️ Warning — No Action Required`",
        "`🔄 Retrying — No Action Required`",
        "`🛠️ Self-Healed — No Action Required`",
        "`🚨 Error — Action Required`",
    },
    "references/interview.md": {
        "**Backtest Strategy**",
        "**Skip Backtesting and Implement on AlphaInsider**",
        "**Build and Run**",
        "**Build, Configure, and Activate**",
        "Creation incomplete",
        "`2×`",
        "`1×`",
    },
    "references/backtesting.md": {
        "Backtest <date or ID>",
        "**Valid**",
        "**Superseded**",
        "**Failed**",
    },
    "references/credentials.md": {
        "scripts/set_env_value.py",
    },
    "references/alphainsider-strategy.md": {
        "`$100,000`",
    },
    "references/automation.md": {
        "**Errors and completed repairs**",
        "**Errors only**",
        "**Errors, completed repairs, and warnings**",
        "scheduler **Run now**",
    },
    "references/scheduled-runs.md": {
        "30 minutes",
    },
    "references/generated-project.md": {
        "Creation incomplete",
        "Strategy created successfully",
        "Strategy automation completed successfully",
        "https://alphainsider.com/resources#automating-trades",
    },
}
FORBIDDEN_STRATEGY_LITERALS = {
    "references/interview.md": {
        "Agree to this strategy",
        "Agree to this backtest plan",
        "Agree to this AlphaInsider setup",
        "Finish here",
        "AlphaInsider permits up to `2×` leverage",
        "Stage 3 selects the actual native automation surface",
    },
    "references/automation.md": {
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
REQUIRED_STRATEGY_BEHAVIORS = {
    "SKILL.md": {
        "plan.md authority": (
            r"`plan\.md`.{0,120}\b(?:source of truth|authoritative)\b"
        ),
        "one strict asset type": (
            r"\bone project\b.{0,100}\bone strategy\b.{0,100}"
            r"`stock`.{0,40}`cryptocurrency`"
        ),
        "native AI scheduler only": (
            r"\buse only\b.{0,100}\bnative AI\b.{0,100}"
            r"\b(?:automation|scheduler)\b"
        ),
        "Draft permits safe discovery": (
            r"\bDraft strategy\b.{0,80}\bpermits?\b.{0,80}"
            r"\binterviewing\b.{0,80}\bread-only discovery\b"
        ),
        "reviewed next step confirms strategy": (
            r"\breviewed next-step choice\b.{0,80}\bconfirms the strategy\b"
        ),
        "stage choices gate execution": (
            r"\bBuild and Run\b.{0,160}\bAuthorized\b.{0,180}"
            r"\bBuild, Configure, and Activate\b.{0,180}\bAuthorized\b"
        ),
        "Complete requires active automation": (
            r"\bCreation is Complete only after\b.{0,180}"
            r"\bnative automation is active\b"
        ),
        "Define verifies scheduler and public execution constraints": (
            r"\bBefore confirming a strategy\b.{0,120}"
            r"\bactual native scheduler\b.{0,120}"
            r"\bpublic AlphaInsider constraints\b.{0,120}"
            r"\bplanned execution operation\b"
        ),
        "scheduler cadence cannot be simulated": (
            r"\bnever keep a run alive\b.{0,100}\bpoll faster\b"
        ),
        "session policy has a documented fallback": (
            r"\bPrefer explicit current session guidance\b"
            r".{0,120}\bwhen absent\b.{0,120}\bstock fallback\b"
            r".{0,120}\b24/7\b"
        ),
        "operational errors keep automation active": (
            r"\bNever pause active automation automatically\b.{0,120}"
            r"\bDegraded/Retrying\b.{0,180}\bnext trigger\b"
        ),
        "backtest findings include visual evidence": (
            r"\bBacktest findings summaries\b.{0,100}\bdata-derived visuals\b"
            r".{0,180}\bEmbed them when supported\b.{0,100}"
            r"\blink directly\b.{0,180}\breport is additional, not a substitute\b"
        ),
    },
    "references/credentials.md": {
        "missing API key is the first action": (
            r"\bmissing key\b.{0,100}\bfirst user action\b"
        ),
        "waiting for a requested key stays in progress": (
            r"\bWaiting for the requested key\b.{0,120}"
            r"\bCreation state In progress\b"
        ),
    },
    "references/user-communication.md": {
        "summary and next step share one prompt": (
            r"\bend of a stage\b.{0,100}\bsummary\b.{0,100}"
            r"\bnext step in the same prompt\b"
        ),
        "forward choice confirms reviewed summary": (
            r"\bforward choice confirms the reviewed summary\b"
        ),
        "no separate agreement question": (
            r"\bNever add a separate agreement question\b"
        ),
        "recommendations are constraint first": (
            r"\bFilter recommendations through known constraints\b.{0,180}"
            r"\bcomplete compatible choices\b.{0,220}"
            r"\bDo not ask how to handle a hypothetical failure\b"
        ),
    },
    "references/interview.md": {
        "backtest is always offered before assessment": (
            r"\bAlways show this choice\b.{0,120}"
            r"\bdo not assess feasibility before\b"
        ),
        "stops never complete creation": (
            r"\bNever set\b.{0,80}\bPhase\b.{0,80}"
            r"\bCreation state\b.{0,80}\bComplete\b.{0,80}"
            r"\bstop or blocker\b"
        ),
        "terminal success has no approval": (
            r"\bStrategy created successfully\b.{0,180}"
            r"\binformational\b.{0,80}\basks for no approval\b"
        ),
        "Define timing uses discovered scheduler": (
            r"\bBefore asking timing questions\b.{0,220}"
            r"\bDefine-time capability discovery\b.{0,700}"
            r"\boffer only complete supported alternatives\b"
        ),
        "Define avoids implementation questions": (
            r"\bDuring Define Strategy ask only\b.{0,160}"
            r"\bdefer credentials and setup decisions\b"
        ),
        "execution operation is mapped internally": (
            r"\bInternally map\b.{0,120}\bAlphaInsider operation\b"
            r".{0,120}\bdo not ask the user to choose an endpoint\b"
        ),
        "allocation side effects are disclosed": (
            r"\bnewOrderAllocations\b.{0,180}\bcancels existing open orders\b"
            r".{0,100}\bcloses positions omitted\b"
        ),
        "exposure guidance is execution specific": (
            r"\bexecution-specific exposure rules\b.{0,180}"
            r"\bnewOrder\b.{0,100}\bno leverage field\b.{0,100}"
            r"\bno documented universal `2×`"
        ),
        "stock sessions use docs then US fallback": (
            r"\bexplicit current rule is authoritative\b.{0,180}"
            r"\bno explicit mapping is published\b.{0,180}"
            r"09:30.{0,80}16:00.{0,80}`America/New_York`"
        ),
        "cryptocurrency sessions are 24/7": (
            r"\bcryptocurrency order availability as 24/7\b.{0,120}"
            r"\bDo not ask a market-session question\b"
        ),
        "compatible recommendations have no hypothetical fallback": (
            r"\bNever offer submission with an expected rejection\b"
            r".{0,180}\bsaved signal with no supported execution time\b"
        ),
        "tier limits stay operation scoped": (
            r"\bApply a public tier limit only to the operation\b"
            r".{0,220}\bminimum documented tier dependency\b.{0,180}"
            r"\bVerify the actual tier only in Stage 3\b"
        ),
        "focused prose discrepancy is retained": (
            r"\bfocused operation prose is stricter than OpenAPI\b"
            r".{0,120}\brecord the discrepancy\b"
        ),
        "implementation does not select timing": (
            r"\bDo not ask the user to select timing here\b.{0,180}"
            r"\breturn the affected timing to Stage 1\b"
        ),
        "terminal title adapts to reuse": (
            r"\bStrategy created successfully\b.{0,180}"
            r"\bStrategy automation completed successfully\b"
        ),
        "results summary includes saved visuals": (
            r"\bInclude the featured run's exact saved result visuals\b"
            r".{0,80}\bresults summary\b.{0,100}\bnot only a link\b"
            r".{0,160}\bEmbed the images when supported\b.{0,100}"
            r"\blink directly to each named image\b"
        ),
        "later creation handoffs reuse result visuals": (
            r"\bReuse those artifacts in every later creation handoff\b"
            r".{0,80}\bpresents the findings\b"
        ),
    },
    "references/backtesting.md": {
        "backtest choice precedes feasibility": (
            r"\bafter the user selects\b.{0,80}\bBacktest Strategy\b"
            r".{0,250}\bfeasibility\b.{0,100}\bfirst\b"
        ),
        "Build and Run gates the test": (
            r"\bOnly the user's\b.{0,40}\bBuild and Run\b.{0,100}"
            r"\bBacktest status\b.{0,30}\bAuthorized\b"
        ),
        "user-directed backtests may run after warning": (
            r"\blet the user choose or suggest any safe\b.{0,100}"
            r"\border-free backtest\b.{0,120}\bChallenge\b.{0,100}"
            r"\bbefore execution\b.{0,80}\brun it\b"
        ),
        "methodology facts are separate from run disposition": (
            r"\bmethodology facts describe\b.{0,160}"
            r"\bseparate disposition\b"
        ),
        "backtest runs preserve recoverable source": (
            r"\bimmutable snapshot\b.{0,100}\bsource and configuration\b"
            r".{0,100}\bexact durable commit\b"
        ),
        "future information is resolved before authorization": (
            r"\banswer may remain\b.{0,60}\bNot assessed\b.{0,120}"
            r"\bmust be\b.{0,60}\bYes\b.{0,30}\bNo\b.{0,100}"
            r"\bAuthorized\b"
        ),
        "future information receives a mandatory results warning": (
            r"\banswer is\b.{0,30}\bYes\b.{0,100}\bbegin with a warning\b"
            r".{0,160}\bcannot demonstrate real-time strategy performance\b"
            r".{0,160}\brepeat that warning beside every affected measurement\b"
        ),
        "each run retains methodology facts": (
            r"\brecord\b.{0,100}\brun's future-information answer\b"
            r".{0,100}\bexact limitations\b"
        ),
        "disclosed approximations retain strategy identity": (
            r"\bmatches the current strategy when it evaluates\b.{0,120}"
            r"\bwithout silently revising intended strategy behavior\b"
            r".{0,220}\bbacktest-only substitute\b.{0,180}"
            r"\bdoes not by itself make the run evidence for a different strategy\b"
        ),
        "every result uses a backtest identity": (
            r"\bIdentify each result as `Backtest <date or ID>"
            r" — Valid \| Superseded \| Failed`"
        ),
        "primary backtest uses implementable cadence": (
            r"\bconfirmed implementable cadence\b.{0,120}"
            r"\bprimary backtest\b.{0,300}\bnative scheduler cannot run\b"
        ),
        "revisions supersede current evidence": (
            r"\bMark affected Valid evidence Superseded\b.{0,220}"
            r"\bHighest completed outcome to Strategy defined\b"
        ),
        "run source remains until explicit deletion": (
            r"\brecoverable source and configuration until\b.{0,100}"
            r"\bexplicitly\b.{0,80}\bdeletion\b"
        ),
        "backtest plan authorizes exact result visuals": (
            r"\bNormally plan two to four data-derived visuals\b.{0,160}"
            r"\bportfolio backtest\b.{0,160}\bequity curve\b.{0,120}"
            r"\bdrawdown\b.{0,180}\bsignal-only backtest\b.{0,180}"
            r"\btwo suitable substitutes\b.{0,220}\breviewed plan before\b"
            r".{0,40}\bBuild and Run\b"
        ),
        "visuals supplement results and direct image links": (
            r"\bSupplement the table and written interpretation\b.{0,120}"
            r"\bsaved result visuals\b.{0,1400}\bEmbed the saved images\b"
            r".{0,120}\blink directly to each named image\b.{0,120}"
            r"\bdetailed report alone is not a substitute\b"
        ),
        "visual artifacts carry standalone context": (
            r"\bstandalone artifact\b.{0,100}\bbacktest identity and period\b"
            r".{0,80}\blabels and units\b.{0,160}"
            r"\balternative text or a caption\b.{0,80}\bone-sentence takeaway\b"
            r".{0,180}\bwarning inside the artifact\b.{0,100}"
            r"\brepeat it beside the visual\b"
        ),
        "visual render failures preserve valid evidence": (
            r"\bplanned visual does not render\b.{0,120}"
            r"\bone safe mechanical repair attempt\b.{0,120}"
            r"\bremaining rendering failure\b.{0,140}\bdoes not\b.{0,100}"
            r"\bevidence Failed\b.{0,260}\blater repair\b.{0,100}"
            r"\bsame saved outputs\b.{0,120}\bnever reruns the trading logic\b"
        ),
        "unavailable visuals receive a terse disclosure": (
            r"\bstate only that some planned visuals are unavailable\b"
        ),
    },
    "references/plan-template.md": {
        "plan records visual selection": (
            r"\bResults to show and charts:\b.{0,120}"
            r"\btwo to four data-derived visuals\b.{0,180}"
            r"\bsignal-only backtest\b"
        ),
        "plan records visual failures and repairs": (
            r"\bBacktest run history\b.{0,300}"
            r"\bvisual-rendering failures and later repairs\b"
        ),
    },
    "references/implementation.md": {
        "stock sessions use docs then fallback": (
            r"\bexplicit current AlphaInsider accepted-session\b.{0,100}"
            r"\bWhen no mapping is published\b.{0,160}"
            r"09:30.{0,120}16:00.{0,80}`America/New_York`"
        ),
        "crypto availability is 24/7": (
            r"\bFor cryptocurrency, treat order availability as 24/7\b"
        ),
        "failed actions wait for another trigger": (
            r"\bfailed external or strategy action ends order-capable work\b"
            r".{0,180}\bnever retry an order in the same trigger\b"
        ),
        "exposure limits are operation specific": (
            r"\bconfirmed maximum exposure\b.{0,160}"
            r"\busing `2×` only where\b.{0,120}"
            r"\ballocation or webhook contract\b"
        ),
        "tier limits are operation specific": (
            r"\bApply a tier limit only to an operation\b.{0,100}"
            r"\bdocumentation explicitly names\b"
        ),
        "tests cannot place or cancel orders": (
            r"\btests\b.{0,80}\bmust not\b.{0,80}\bsubmit\b"
            r".{0,30}\bcancel\b.{0,100}\border\b"
        ),
    },
    "references/automation.md": {
        "cron is prohibited": r"\bnever\b.{0,80}\bcron\b",
        "errors-only notifications are recommended": (
            r"\bErrors only\b.{0,80}\brecommended\b"
        ),
        "notification choices put errors only first": (
            r"\bwhich events\b.{0,120}\bErrors only\b.{0,200}"
            r"\bErrors and completed repairs\b.{0,120}"
            r"\bErrors, completed repairs, and warnings\b"
        ),
        "unsupported frequency requires user selection": (
            r"\brequested (?:frequency|cadence)\b.{0,100}\bunavailable\b"
            r".{0,180}\bask\b.{0,80}\buser\b.{0,40}"
            r"\b(?:select|choose)\b"
        ),
        "description is ready before activation": (
            r"\bactivate only after\b.{0,120}\bdescription\b"
        ),
        "setup notifications are not sent": (
            r"\bnever send\b.{0,80}\bsetup or test notification\b"
        ),
        "unverifiable notification choice is retained": (
            r"\bsupport cannot be checked\b.{0,120}\baccept\b.{0,80}"
            r"\buser-selected, unverified\b"
        ),
        "notification delivery is not an activation gate": (
            r"\bNotification delivery is not an activation gate\b"
        ),
        "Define discovers actual scheduler before timing": (
            r"\bBefore asking strategy timing questions\b.{0,120}"
            r"\bactual current platform\b.{0,120}\bofficial scheduler\b"
        ),
        "Define offers supported schedules only": (
            r"\bcomplete compatible timing choices\b.{0,500}"
            r"\bnearest complete supported alternatives\b"
        ),
        "faster cadence workarounds are prohibited": (
            r"\bNever simulate a faster cadence\b.{0,180}"
            r"\bpolling\b.{0,120}\bbackground process\b"
        ),
        "undocumented stock sessions use US fallback": (
            r"\bAn exchange-status name or example is not proof\b"
            r".{0,180}\bWhen the sources publish no mapping\b.{0,180}"
            r"09:30.{0,120}16:00"
        ),
        "crypto session questions are omitted": (
            r"\bcryptocurrency order availability as 24/7\b.{0,100}"
            r"\bDo not ask a cryptocurrency market-session question\b"
        ),
        "compatible timing avoids hypothetical fallback": (
            r"\bDo not ask a hypothetical fallback question\b.{0,100}"
            r"\bcompatible choice\b"
        ),
        "Define does not inspect account": (
            r"\bDo not request a key\b.{0,100}"
            r"\binspect the user's account tier\b"
        ),
        "implementation drift returns to Define": (
            r"\bDo not reselect timing during implementation\b.{0,180}"
            r"\breturn the schedule decision to Draft in Define Strategy\b"
        ),
        "notification repair requires enabled scope": (
            r"\bAttempt a bounded channel repair\b.{0,160}"
            r"\bself-healing is enabled\b.{0,100}"
            r"\bnotification repair is inside its confirmed scope\b"
        ),
        "notification repair scope is explicitly chosen": (
            r"\bAsk explicitly whether notification channel repair\b"
            r".{0,100}\binside that scope\b.{0,160}"
            r"\bdisabled unless both self-healing and that scope are confirmed\b"
        ),
    },
    "references/scheduled-runs.md": {
        "dry runs require an explicit chat request": (
            r"\bdry run\b.{0,80}\bonly\b.{0,80}"
            r"\bexplicit chat request\b"
        ),
        "performance is not run health": (
            r"\b(?:profit|loss|return|win rate)\b.{0,180}"
            r"\bnot a health criterion\b"
        ),
        "operational errors keep automation active": (
            r"\boperational error never pauses native automation automatically\b"
            r".{0,180}\bAutomation state\b.{0,60}\bPaused\b"
        ),
        "errors become degraded next-trigger retries": (
            r"\bFor every error\b.{0,500}\bDegraded/Retrying\b"
            r".{0,160}\bnext scheduled retry\b"
        ),
        "ambiguous orders gate later orders": (
            r"\border might have reached AlphaInsider\b.{0,100}"
            r"\bnever assume success or failure\b.{0,220}"
            r"\bsubmits nothing while ambiguity remains\b"
        ),
        "recovery does not replay orders": (
            r"\bnext trigger\b.{0,220}\brecompute from current inputs\b"
            r".{0,120}\bNever replay a missed signal or order\b"
        ),
        "repairs need new evidence": (
            r"\battempt another repair only when new evidence\b.{0,160}"
            r"\bNever repeat the same failed repair\b"
        ),
        "duplicate error notifications are suppressed": (
            r"\bSend the first enabled notification\b.{0,220}"
            r"\bSuppress an equivalent repeat\b"
        ),
        "leftover-lock removal requires proof": (
            r"\bnever remove a leftover lock\b.{0,120}\bchecks prove\b"
            r".{0,100}\bowning run\b.{0,40}\bnot active\b"
        ),
        "notification failure does not pause trading": (
            r"\bnotification failure\b.{0,80}\bnever pauses\b.{0,80}"
            r"\btrading\b"
        ),
        "notification channels fail independently": (
            r"\bconfigured channels independently\b.{0,100}"
            r"\bWorking channels send\b"
        ),
        "errors-only notifications send retrying and action errors": (
            r"\bErrors only\b.{0,80}\bsends\b.{0,60}"
            r"\bRetrying and Error events\b"
        ),
        "one trigger cannot simulate faster cadence": (
            r"\bEach trigger performs at most one strategy run\b.{0,180}"
            r"\bimitate a cadence faster\b"
        ),
        "notification repair requires enabled scope": (
            r"\blimited channel repair\b.{0,140}"
            r"\bself-healing is enabled\b.{0,100}"
            r"\bnotification repair is inside its confirmed scope\b"
        ),
    },
    "references/plan-template.md": {
        "errors-only notifications are recommended": (
            r"\bNotification events\b.{0,200}\berrors only\b.{0,80}"
            r"\brecommended\b"
        ),
        "operational health is separate from automation": (
            r"\bAutomation state\b.{0,180}\bOperational health\b.{0,120}"
            r"\bDegraded/Retrying\b"
        ),
    },
    "references/project-root.md": {
        "Complete transition is cross-field verified": (
            r"\bCreation state can first transition to Complete only when\b"
            r".{0,300}"
            r"\bAutomation state is Active\b"
        ),
        "runtime errors preserve active completed creation": (
            r"\blater operational error does not undo completed creation\b"
            r".{0,120}\bAutomation state Active\b.{0,120}"
            r"\bDegraded/Retrying\b"
        ),
        "legacy plans remain resumable": (
            r"\bformer \*\*Plan agreement\*\* field\b.{0,420}\blegacy version\b"
            r".{0,120}\bnot an unrelated directory\b"
        ),
        "legacy plans cannot be promoted": (
            r"\bNever promote ambiguous legacy work\b.{0,120}"
            r"\bAuthorized, Active, or Complete\b"
        ),
        "project env is conditional": (
            r"`\.env` file is conditional\b.{0,100}"
            r"\bnot part of a new project's required initial layout\b"
        ),
        "legacy migration has timestamped backup": (
            r"\bBefore changing `plan\.md`.{0,120}"
            r"plan-before-schema-migration-YYYYMMDDTHHMMSSZ\.md"
            r".{0,260}\bNever overwrite a prior backup\b"
        ),
        "legacy leverage becomes operation-specific exposure": (
            r"\bTranslate an old leverage value\b.{0,160}"
            r"\b(?:not|without)\b.{0,100}\buniversal AlphaInsider limit\b"
            r".{0,260}\bcurrent order operation\b"
        ),
    },
    "references/changes-and-deletion.md": {
        "full deletion leaves no tombstone": (
            r"\bfull deletion\b.{0,100}\bremove\b.{0,80}"
            r"\bentire selected project\b.{0,80}\bno tombstone\b"
        ),
        "strategy revisions supersede affected evidence": (
            r"\bmark every affected Valid backtest run Superseded\b"
            r".{0,180}\bcurrent outcome to Strategy defined\b"
        ),
        "backtest source needs explicit deletion": (
            r"\bnever authorize deletion\b.{0,160}"
            r"\bbacktest source or configuration\b"
        ),
    },
    "references/generated-project.md": {
        "generated guide forbids complete env inspection": (
            r"\bforbid\b.{0,120}\b(?:opening|inspecting)\b.{0,80}"
            r"\bcomplete `\.env`"
        ),
        "generated guide protects update and remote settings": (
            r"`pending-update\.md`.{0,120}"
            r"\bAlphaInsider strategy identity and settings\b"
            r".{0,120}\bscheduler identity and frequency\b"
        ),
        "generated outputs warn about future information": (
            r"\bWhen future-information use is\b.{0,30}\bYes\b.{0,80}"
            r"\bmandatory warning\b.{0,80}\bbefore backtest results\b"
            r".{0,80}\bbeside every affected measurement\b"
        ),
        "incomplete handoff omits broker resource": (
            r"\bCreation incomplete\b.{0,2200}\bDo not show the broker resource\b"
        ),
        "runtime errors are not incomplete creation": (
            r"\bDo not use this handoff\b.{0,100}\boperational error\b"
            r".{0,100}\bcreation already completed\b"
        ),
        "generated runbook keeps automation active on errors": (
            r"\boperational error ends order work for that trigger\b"
            r".{0,160}\bAutomation state Active\b.{0,100}"
            r"\bDegraded/Retrying\b"
        ),
        "terminal wording adapts to strategy reuse": (
            r"\bStrategy created successfully\b.{0,180}"
            r"\bStrategy automation completed successfully\b"
        ),
        "backtest handoffs reuse and directly present visuals": (
            r"\bWhenever an incomplete or terminal handoff presents backtest findings\b"
            r".{0,120}\breuse the exact saved result visuals\b.{0,180}"
            r"\bEmbed them when supported\b.{0,100}"
            r"\blink directly to each named image\b.{0,120}"
            r"\breport link is additional and never replaces\b"
        ),
        "backtest handoffs preserve visual failure handling": (
            r"\bplanned visual remains unavailable\b.{0,100}"
            r"\bstate only that some planned visuals are unavailable\b"
            r".{0,220}\bsame saved run outputs\b.{0,100}"
            r"\bpreserve the original failure record\b"
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

    for owner, behaviors in REQUIRED_STRATEGY_BEHAVIORS.items():
        owner_text = " ".join(strategy_source_texts[owner].split())
        missing_behaviors = {
            name
            for name, pattern in behaviors.items()
            if re.search(pattern, owner_text, re.IGNORECASE) is None
        }
        if missing_behaviors:
            errors.append(
                f"strategy-creator {owner} is missing behavioral contracts "
                f"{sorted(missing_behaviors)}"
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

    plan_lines = plan_text.splitlines()
    plan_field_lines = {
        field: [line for line in plan_lines if line.startswith(field)]
        for field in REQUIRED_PLAN_FIELDS
    }
    missing_plan_fields = {
        field for field, lines in plan_field_lines.items() if not lines
    }
    if missing_plan_fields:
        errors.append(
            "strategy plan template is missing fields "
            f"{sorted(missing_plan_fields)}"
        )

    duplicate_plan_fields = {
        field for field, lines in plan_field_lines.items() if len(lines) > 1
    }
    if duplicate_plan_fields:
        errors.append(
            "strategy plan template repeats fields "
            f"{sorted(duplicate_plan_fields)}"
        )

    fields_without_inline_values = {
        field
        for field, lines in plan_field_lines.items()
        if lines
        and not lines[0][len(field) :].split("<!--", 1)[0].strip()
    }
    if fields_without_inline_values:
        errors.append(
            "strategy plan template fields need values on their field lines "
            f"{sorted(fields_without_inline_values)}"
        )

    invalid_plan_enums: dict[str, tuple[str, ...] | None] = {}
    invalid_plan_defaults: dict[str, str] = {}
    for field, expected_values in REQUIRED_PLAN_ENUMS.items():
        lines = plan_field_lines.get(field, [])
        if not lines:
            continue
        line = lines[0]
        comment = re.search(r"<!--\s*(.*?)\s*-->", line)
        actual_values = (
            tuple(value.strip() for value in comment.group(1).split("|"))
            if comment
            else None
        )
        if actual_values != expected_values:
            invalid_plan_enums[field] = actual_values

        default_value = line[len(field) :].split("<!--", 1)[0].strip()
        if default_value not in expected_values:
            invalid_plan_defaults[field] = default_value

    if invalid_plan_enums:
        errors.append(
            "strategy plan template has invalid status enums "
            f"{invalid_plan_enums}"
        )
    if invalid_plan_defaults:
        errors.append(
            "strategy plan template has invalid status defaults "
            f"{invalid_plan_defaults}"
        )

    invalid_plan_contract_enums: dict[str, tuple[str, ...] | None] = {}
    for field, expected_values in REQUIRED_PLAN_COMMENT_ENUMS.items():
        lines = plan_field_lines.get(field, [])
        if not lines:
            continue
        comment = re.search(r"<!--\s*(.*?)\s*-->", lines[0])
        actual_values = (
            tuple(value.strip() for value in comment.group(1).split("|"))
            if comment
            else None
        )
        if actual_values != expected_values:
            invalid_plan_contract_enums[field] = actual_values
    if invalid_plan_contract_enums:
        errors.append(
            "strategy plan template has invalid workflow enums "
            f"{invalid_plan_contract_enums}"
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

    interview_text = reference_texts["interview.md"]
    interview_phase_positions = [
        interview_text.find(phase) for phase in REQUIRED_INTERVIEW_PHASE_ORDER
    ]
    if -1 in interview_phase_positions or interview_phase_positions != sorted(
        interview_phase_positions
    ):
        errors.append(
            "strategy interview phases must use order "
            f"{list(REQUIRED_INTERVIEW_PHASE_ORDER)}"
        )

    alpha_setup_section_positions = [
        interview_text.find(section)
        for section in REQUIRED_ALPHA_SETUP_SECTION_ORDER
    ]
    if (
        -1 in alpha_setup_section_positions
        or alpha_setup_section_positions
        != sorted(alpha_setup_section_positions)
        or any(
            interview_text.splitlines().count(section) != 1
            for section in REQUIRED_ALPHA_SETUP_SECTION_ORDER
        )
    ):
        errors.append(
            "strategy AlphaInsider setup interview must use section order "
            f"{list(REQUIRED_ALPHA_SETUP_SECTION_ORDER)}"
        )
    else:
        access_start, strategy_start, implementation_start, review_start = (
            alpha_setup_section_positions
        )
        alpha_setup_routes = {
            "credentials.md": interview_text[access_start:strategy_start],
            "alphainsider-strategy.md": interview_text[
                strategy_start:implementation_start
            ],
            "automation.md": interview_text[
                implementation_start:review_start
            ],
        }
        missing_alpha_setup_routes = {
            route
            for route, section in alpha_setup_routes.items()
            if route not in section
        }
        if missing_alpha_setup_routes:
            errors.append(
                "strategy AlphaInsider setup sections are missing routes "
                f"{sorted(missing_alpha_setup_routes)}"
            )

    implementation_text = reference_texts["implementation.md"]
    if implementation_text.splitlines().count(
        "## AlphaInsider compatibility"
    ) != 1:
        errors.append(
            "strategy implementation must define one AlphaInsider "
            "compatibility section"
        )

    project_root_text = reference_texts["project-root.md"]
    missing_layout_entries = {
        entry for entry in REQUIRED_CORE_LAYOUT if entry not in project_root_text
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
