#!/usr/bin/env python3
"""Validate the public AlphaInsider skill catalog."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
EXPECTED_SKILLS = {"alphainsider", "strategy-creator"}
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
        ("verifyToken", "POST", "/verifyToken"),
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
    "alphainsider-target.md",
    "cleanup.md",
    "credentials.md",
    "implementation.md",
    "interview.md",
    "operation-and-scheduling.md",
    "plan-template.md",
    "versioning.md",
}
REQUIRED_STRATEGY_RELEASES = {
    "1.0.0",
    "1.1.0",
    "1.2.0",
    "1.3.0",
    "1.3.1",
    "1.4.0",
    "1.4.1",
    "1.4.2",
    "1.5.0",
    "1.5.1",
    "1.6.0",
    "1.7.0",
    "1.8.0",
    "2.0.0",
}
STRATEGY_SKILL_MAX_WORDS = 950
REQUIRED_PROGRESSIVE_DISCLOSURE_GUIDANCE = {
    "Do not preload every reference",
    "Read each file in full only when its phase or action begins",
}
EXPECTED_STRATEGY_SCRIPTS = {"check_for_update.py", "set_env_value.py"}
EXPECTED_PLAN_STATES = {"draft", "confirmed", "implemented", "retired"}
STRICT_SEMVER_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
)
STRATEGY_VERSION_FILE_PATTERN = re.compile(r"^v([1-9][0-9]*)\.md$")
REQUIRED_PLAN_SECTION_ORDER = (
    "# Strategy Plan",
    "## Objective",
    "## Market and instruments",
    "## Strategy behavior",
    "## Data and resources",
    "## Execution and risk",
    "## Backtesting",
    "## Implementation",
    "## Operation and scheduling",
    "## AlphaInsider target",
    "## Confirmation",
)
REQUIRED_PLAN_SECTIONS = set(REQUIRED_PLAN_SECTION_ORDER)
REQUIRED_INTERVIEW_PHASE_ORDER = (
    "1. **Objective**",
    "2. **Market and instruments**",
    "3. **Strategy behavior**",
    "4. **Data and resources**",
    "5. **Execution and risk**",
    "6. **Backtesting**",
    "7. **Implementation**",
    "8. **Operation and scheduling**",
    "9. **AlphaInsider target**",
)
REQUIRED_PLAIN_LANGUAGE_PLAN_FIELDS = {
    "- Goal:",
    "- Automatic pause or shutdown conditions and logging:",
    "- Exact create, modify, overwrite, delete, stop, pause, disable, activation, promotion, provisioning, synchronization, ID-persistence, native-operation, and agent-task actions:",
    "- Managed artifact inventory and retirement state:",
    "- Tests to run and expected results:",
}
REQUIRED_TARGET_PLAN_FIELDS = {
    "- Target readiness:",
    "- Local-only reason:",
    "- Target source:",
    "- Owned-strategy discovery:",
    "- Proposed strategy name:",
    "- Owner starting balance:",
    "- Access eligibility and mode:",
    "- Paid cryptocurrency launch price:",
    "- AlphaInsider strategy ID:",
    "- Remote disposition:",
    "- Pending outgoing strategy ID and result:",
    "- Generated AlphaInsider description:",
    "- Description synchronization:",
    "- Target lifecycle disposition:",
}
REQUIRED_OPERATION_PLAN_FIELDS = {
    "- Operation mode:",
    "- Invocation model:",
    "- Cadence, timezone, precision, and worst-case cycle duration:",
    "- Capability check and selected runner or environment:",
    "- Resource identifier and exact native definitions or agent task:",
    "- Missed-run or catch-up behavior and acceptance:",
    "- Initial activation and autostart:",
    "- Overlap, retry, and persistent-service restart policy:",
    "- Logs, run history, notifications, rotation, and retention:",
    "- Installation state and next scheduled run:",
    "- Operation cleanup state and removal verification:",
}
REQUIRED_GRILL_PROTOCOL_GUIDANCE = {
    "Ask every currently unblocked user decision in one turn",
    "interactive question prompt",
    "not ordinary chat text",
    "recommended option first",
    "Research repository, API, host, and provider facts",
    "A question that depends on an answer still open in this round",
    "Do not depend on any other skill for this pacing",
}
REMOVED_PLAN_FIELDS = {
    "- Why the strategy could work:",
    "- When results will be reviewed:",
    "- What would show the strategy is working:",
    "- What would show the strategy needs changes or should stop:",
    "- User confirmation:",
    "- Confirmation time:",
    "- Core creation fields approval:",
    "- Continuous-command mode:",
    "- Manager, identifier, and capability check:",
    "- User-level host definition:",
    "- Login autostart:",
    "- Failure restart policy and bounded parameters:",
    "- Log exposure, paths, rotation, and retention:",
    "- Installation state:",
    "- Deferred reason:",
    "- Failed-current-run target cleanup:",
}
REMOVED_PLAN_SECTIONS = {"## Background operation"}
REMOVED_INTERVIEW_PHASES = {"8. **Background operation**"}
REMOVED_INTERVIEW_QUESTIONS = {
    "Why do you think this trading idea could work?",
    "After how much time or how many trades should we review the results?",
    "What results would tell you the strategy is working?",
    "What loss or behavior would make you change or stop it?",
}
REMOVED_TARGET_ORDER_GUIDANCE = {
    "Complete its permission gate before the interview",
    "before the strategy interview",
    "resolve the target before instrument selection",
    "pause all interview, remote creation, and implementation work",
    "after strategy design and background-operation planning and before backtesting",
    "backtesting planning may continue",
    "continue through backtesting and plan confirmation",
    "after strategy, backtesting, implementation-contract, and background-operation planning",
}
REMOVED_SEPARATE_CONFIRMATION_GUIDANCE = {
    "Obtain explicit core creation approval",
    "Changing any core field invalidates that approval",
    "record approved core fields for a new target",
}
REMOVED_POST_CONFIRMATION_APPROVAL_GUIDANCE = {
    "does not authorize deletion, plan promotion, or implementation",
    "separate explicit approval",
    "Plan confirmation and deletion approval are separate decisions",
    "an existing file still requires explicit overwrite approval",
    "Request one explicit approval for that inventory",
    "Request renewed approval before touching any newly discovered path",
    "ask whether to delete this exact strategy",
    "If the user approves cleanup",
    "approval-gated failed-creation cleanup only",
    "separate deletion-approval gate",
    "do not combine plan confirmation with deletion approval",
}
REMOVED_TARGET_DELETION_GUIDANCE = {
    "Never delete a selected existing strategy",
    "failed-current-run cleanup only",
    "never authorizes routine deletion or deletion of a selected existing strategy",
}
REQUIRED_REPLACEMENT_GUIDANCE = {
    "every section heading from the current plan template",
    "update the existing plan",
    "replace the trading strategy with a new one",
    "`docs/replacement-plan.md`",
    "Show and record every exact deletion, overwrite, promotion",
    "final confirmation sets them to `confirmed`",
    "authorizes the exact recorded deletion, promotion, cleanup, and implementation actions",
    "perform only the recorded actions",
    "Never recursively delete the project root",
    "Never delete `.env`",
    "replace `docs/plan.md` with `docs/replacement-plan.md`",
}
REQUIRED_CREDENTIAL_GUIDANCE = {
    "`scripts/set_env_value.py`",
    "`scripts/alphainsider_request.py`",
    "`scripts/alphainsider_stream.py`",
    "Recommend that the user add the values to `.env` themselves",
    "they may paste the values in chat",
    "pasting credentials is less secure",
    "the value is visible to the agent",
    "tool metadata",
    "transient process listing",
    "`set_env_value.py NAME VALUE`",
    "pass the complete value as exactly one argument",
    "structured argument-array",
    "quote the value as one literal argument",
    "Never show this command to the user",
    "Do not open `.env` before or after the update",
    "approval to update only those names",
    "use the sibling request helper",
    "--remove ALPHAINSIDER_STRATEGY_ID",
    "agent-only helper",
    "Never import the helper",
    "reproduce its write logic",
    "shell pipeline, redirect",
    "environment or shell variable",
    "temporary file",
    "direct `.env` edit",
    "without requesting another approval",
    "never recover it from `.env`",
    "runtime cannot pass it as one safely quoted argument",
    "return to the user-edit workflow",
    "Do not improvise another write path",
    "`--remove NAME` receives no value and is also agent-only",
    "Generated `README.md` files must preserve user editing",
    "never show the helper command",
    "Generated `AGENTS.md` files must point at the installed skill",
}
REMOVED_LIVE_INPUT_CREDENTIAL_GUIDANCE = {
    "interactive terminal",
    "live process-input",
    "live-input workflow",
    "non-echoing prompt",
    "process-input channel",
    "readiness prompt",
}
REQUIRED_STRATEGY_API_PERMISSIONS = (
    "getUserInfo",
    "getStrategies",
    "getStrategyValues",
    "getUserStrategies",
    "getStrategyPerformance",
    "getRecommendedStrategies",
    "searchStrategies",
    "newStrategy",
    "updateStrategy",
    "deleteStrategy",
    "getStrategySubscriptions",
    "getStrategyCalculation",
    "getAccountSubscription",
    "getTimelines",
    "getStrategyTimelines",
    "newPost",
    "previewPost",
    "deletePost",
    "getPositions",
    "getOrders",
    "getMaxOrderSize",
    "newOrder",
    "newOrderAllocations",
    "deleteOrder",
    "wsStockPrice",
    "wsStrategyValue",
    "wsOrders",
    "wsPositions",
    "wsTimelines",
)
REQUIRED_PROVISIONING_GUIDANCE = {
    "https://alphainsider.com/settings/developers",
    "selecting the **AI Agent** preset",
    "`verifyToken` has no selectable permission",
    "stock REST lookup endpoints require no API-key permission",
    "`like` and `unlike` are not required",
    "subscription permissions are read-only",
    "list only the missing permission names",
    "pause AlphaInsider target setup and every remote action",
    "use the verified token's `user_id` with `getUserStrategies`",
    "Never pick the first result or create a duplicate silently",
    "Persist the user's selection",
    "Compare the owned strategy count with `limits.max_strategies`",
    "stop if either eligibility check fails",
    "`getAccountSubscription.level > 0`",
    "`getUserInfo.verified` is true",
    "record public access without an extra access question",
    "Never offer paid stock creation",
    "$10 through $1000",
    "public to `private: false, price: 0`",
    "private to `private: true, price: 0`",
    "Do not ask for separate creation approval",
    "Changing a core field before confirmation updates the draft",
    "changing one after confirmation returns the plan to `draft`",
    "Do not call `newStrategy` before complete plan confirmation",
    "one to three plain-language sentences",
    "write it only to `ALPHAINSIDER_STRATEGY_ID`",
    "report it once",
    "retain the created target and saved ID",
    "Never request another skill-level approval",
    "Only after deletion succeeds",
    "Never remove a default that now refers to another strategy",
    "send the current name and owner `input_value` unchanged",
    "If synchronization fails, leave the plan `confirmed`",
}
REQUIRED_CLEANUP_GUIDANCE = {
    "The active or replacement plan is the sole place",
    "Before setting `implemented`",
    "exact project-relative managed-artifact inventory",
    "retain and detach",
    "selected existing owned targets",
    "Disable future cycles",
    "safe cycle boundary",
    "preventing another internal cycle",
    "releasing its runtime marker",
    "never force-kill an uncertain process",
    "getStrategySubscriptions",
    "open orders",
    "nonzero positions",
    "does not state whether or how those resources cascade",
    "never calls `newOrder`",
    "never calls `deleteOrder`",
    "verify that the target no longer resolves",
    "Never recursively delete the project root",
    "`.env`, `.gitignore`",
    "`status: retired`",
    "If the replacement target is local-only",
    "allow its confirmed future activation with a prominent pending-cleanup warning",
    "never retry it during unrelated work",
    "pending outgoing strategy ID",
}
REQUIRED_SINGLE_CONFIRMATION_GUIDANCE = {
    "Complete plan confirmation is the only skill-level execution approval",
    "authorizes every exact planned create, modify, overwrite, delete, stop, pause, disable, activation, promotion, provisioning, ID-persistence, synchronization, build, native-operation, and agent-task action",
    "never request another approval for a confirmed action",
    "If any required action, identity, or path was absent or changes afterward, return the plan to `draft`",
    "exact action, and ask once for final confirmation",
    "Never request a one-off approval against a confirmed plan",
    "sole authorization for `newStrategy`",
    "sole authorization to call `newStrategy` and persist the returned strategy ID",
    "do not ask again",
    "must not prompt for confirmation before submitting planned paper orders",
    "Running either command is the user's execution action",
    "Never manually run a one-cycle command, start a persistent process, or trigger a scheduled task during build or verification",
}
REQUIRED_LOCAL_ONLY_TARGET_GUIDANCE = {
    "after strategy, backtesting, implementation-contract, and operation-and-scheduling planning as the final AlphaInsider forward-test setup phase before confirmation",
    "offer a compatible owned target or a new target",
    "target readiness",
    "`ready` or `local-only`",
    "preserve every completed earlier planning decision",
    "continue to plan confirmation",
    "complete local build",
    "Make no remote calls",
    "mark them unavailable until target readiness is resolved",
    "keep the plan `confirmed`",
    "never `implemented`",
    "return the plan to `draft`",
    "reconfirm the complete plan",
    "return to target setup before confirmation",
}
REQUIRED_OPERATION_GUIDANCE = {
    "Separate how long the strategy operates from how long one process lives",
    "a `single run` executes one decision cycle",
    "a `persistent process` stays visible or managed and performs cycles itself",
    "a `recurring schedule` invokes the finite one-cycle command at each planned interval",
    "Always present `foreground`",
    "Linux systemd and macOS launchd may run a persistent process or recurring finite cycles",
    "Windows Task Scheduler supports only recurring finite cycles",
    "Recommend a compatible `background process` runner before an `agent scheduler`",
    "Never omit a family",
    "Inspect those tools",
    "worst-case cycle duration is shorter than the interval",
    "require the user's acceptance",
    "Recurring one-cycle execution cannot overlap",
    "fail-closed process-lifetime lock",
    "Scheduler-level retries and task-level restart-on-failure are disabled",
    "default agent-task notifications to failures only",
    "Never put credentials",
    "Never overwrite an active unrelated resource",
    "allow an active cycle to reach a safe completion",
    "~/.config/systemd/user/<identifier>.service",
    "~/.config/systemd/user/<identifier>.timer",
    "`Type=oneshot` with `Restart=no`",
    "`StartCalendarInterval`",
    "`MultipleInstancesPolicy`",
    "Do not require a named agent product, proprietary task schema, or vendor-specific conversation type",
    "does not mean skip this agent's own scheduler or automation tools",
    "Prefer the confirmed persistent project rather than an ephemeral or isolated copy",
    "already available durable runtime",
    "Do not provision cloud infrastructure",
    "recorded limitations, not reasons to hide the family",
    "create the task even when project access, runtime, or durability is missing",
    "run the exact confirmed one-cycle invocation once",
    "Never manually trigger a run during creation or validation",
    "recommend active",
    "create no native definition or agent task",
    "not an immediate test run",
}
REMOVED_CURRENT_OPERATION_GUIDANCE = {
    "Offer tmux only when it is installed",
    "a one-cycle command always remains foreground-only",
    "tmux is manual-only",
    "offer only usable runners",
    "Offer `agent scheduled task` only when",
    "native user-system",
    "independent recurring scheduled task whose saved instruction and lifecycle do not depend on the planning conversation",
}
FORBIDDEN_AGENT_SCHEDULER_VENDOR_TERMS = {
    "ChatGPT",
    "Codex",
    "OpenAI",
    "RRULE",
    "automation_update",
    "thread-attached heartbeat",
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
    "Before finalizing any change under `skills/alphainsider/`",
    "https://api.alphainsider.com/llms.txt",
    "https://api.alphainsider.com/openapi.yaml",
    "https://api.alphainsider.com/asyncapi.yaml",
    "Reconcile every discrepancy in the same change",
}
REQUIRED_STARTUP_GUIDANCE = {
    "a short `## Start` section",
    "ordered, copy-paste commands",
    "dependency installation and `.env` preparation",
    "a single cycle, persistent operation when available, and recurring scheduling equally",
    "Match the selected language",
    "`source .venv/bin/activate` immediately before the execution commands",
    "the project's exact package-manager and runtime commands",
}
REQUIRED_EXPOSURE_GUIDANCE = {
    "100% is 1× portfolio value",
    "up to 200% (2×)",
    "platform ceiling, not a default",
    "do not assume 100% is the platform maximum",
    "Record the user's chosen cap",
    "`getMaxOrderSize`",
}
REQUIRED_MARKET_DATA_GUIDANCE = {
    "Prefer AlphaInsider's applicable stock REST endpoints and `wsStockPrice`",
    "supported current instrument metadata, exchange status, and bid, ask, or last prices",
    "Use an external provider when AlphaInsider does not supply the required live",
    "For historical inputs used by live operation",
    "compare AlphaInsider and external sources case by case",
    "Never use AlphaInsider's `getStockPriceHistory` for a backtest",
    "Require a credible external historical source",
    "mark backtesting unavailable",
    "same decision-logic input contract",
    "timestamp, symbol, price-adjustment, and coverage differences",
}
REQUIRED_VERSION_GUIDANCE = {
    "`scripts/check_for_update.py` once at the start of every invocation",
    "never run its update command or ask for permission to run it",
    "`MAJOR.MINOR.PATCH`",
    "Increment the version for every published Strategy Creator change",
    "Treat that exact legacy shape as `0.0.0`",
    "Compare the project with the installed version",
    "never a remote version",
    "npx skills@latest update alphainsider strategy-creator",
    "one `vN.md` file per major version",
    "Select every documented release greater than",
    "less than or equal to the installed version",
    "Process the selected release sections in ascending semantic-version order",
    "Audit the project against the installed skill",
    "Combine all selected increments into one target audit",
    "every exact create, modify, and delete path",
    "Final complete-plan confirmation is the sole authorization for the exact recorded upgrade actions",
    "instead of requesting a one-off approval",
    "Advance `contract_version` only after",
    "do not write intermediate contract versions",
    "interrupted or failed upgrade",
    "For a version-only upgrade, classify the configured target as an existing strategy",
    "do not create a strategy or sync its description",
    "The upgrade alone does not require runtime-code or dependency changes",
    "Pass `reconnect=True` to `stream_events` when the plan requires continuous reconnection and re-subscription",
    "retain the default one-session behavior when the plan requires the strategy to stop on a stream error",
}
REQUIRED_STRATEGY_VERSION_LAYOUT_GUIDANCE = {
    "sole nested exception",
    "`references/versions/vN.md`",
    "highest documented release",
}
REQUIRED_UPDATE_CHECKER_SOURCE = {
    "https://raw.githubusercontent.com/AlphaInsider/skills/master/",
    "skills/strategy-creator/references/versioning.md",
    'UPDATE_COMMAND = "npx skills@latest update alphainsider strategy-creator"',
    "TIMEOUT_SECONDS = 3",
    "MAX_RESPONSE_BYTES = 64 * 1024",
    "response.geturl() != REMOTE_VERSION_URL",
}
README_MAX_WORDS = 450
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
    "`strategy-creator`",
    "npx skills@latest add",
    "`docs/plan.md`",
    "paper-trading",
    "Credentials remain",
    "agent-only",
    "offline tests",
    "language-specific `Start` section",
    "sole approval for every exact planned implementation or update action",
    "without another approval",
    "never submits AlphaInsider orders",
    "prefer it for supported current market data",
    "Backtests require credible external history",
    "`contract_version`",
    "npx skills@latest update alphainsider strategy-creator",
    "never installed automatically",
    "verifies its required API-key permissions",
    "**AI Agent** preset",
    "discovers owned strategies",
    "syncs the confirmed description",
    "`references/versions/vN.md`",
    "final-confirmation upgrade",
    "Operation and scheduling",
    "user-level systemd or launchd",
    "Windows Task Scheduler",
    "or an agent scheduler",
    "default active",
    "retain and detach",
    "retired audit plan",
    "never cancels orders, liquidates positions",
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


def semver_tuple(value: str) -> tuple[int, int, int] | None:
    match = STRICT_SEMVER_PATTERN.fullmatch(value)
    if match is None:
        return None
    return tuple(int(part) for part in match.groups())


def markdown_section_lines(text: str, heading: str) -> list[str] | None:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        return None
    return [line.strip() for line in match.group("body").splitlines() if line.strip()]


def validate_strategy_version_history(
    version_text: str,
    version_files: dict[str, str],
    current_version: str | None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    release_versions: list[str] = []
    major_files: list[tuple[int, str, str]] = []

    for relative_path, text in version_files.items():
        match = STRATEGY_VERSION_FILE_PATTERN.fullmatch(relative_path)
        if match is None:
            errors.append(
                "strategy version logs must use references/versions/vN.md: "
                f"{relative_path}"
            )
            continue
        major_files.append((int(match.group(1)), relative_path, text))

    major_files.sort(key=lambda item: item[0])
    expected_index = [
        f"- [Version {major}](versions/{relative_path})"
        for major, relative_path, _text in major_files
    ]
    actual_index = markdown_section_lines(version_text, "Version logs")
    if actual_index != expected_index:
        errors.append(
            "strategy version index must link every major-version log exactly "
            "once in ascending order"
        )

    for major, relative_path, text in major_files:
        title = f"# Strategy Creator Version {major}"
        if text.splitlines().count(title) != 1:
            errors.append(
                f"strategy version log {relative_path} must contain exactly "
                f"one {title!r} heading"
            )

        headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
        if not headings or headings[0] != "Contents" or headings.count("Contents") != 1:
            errors.append(
                f"strategy version log {relative_path} must start with one "
                "Contents section"
            )
        release_headings = [heading for heading in headings if heading != "Contents"]
        parsed_releases: list[tuple[int, int, int]] = []
        for release in release_headings:
            parsed = semver_tuple(release)
            if parsed is None:
                errors.append(
                    f"strategy version log {relative_path} has malformed "
                    f"release heading {release!r}"
                )
                continue
            if parsed[0] != major:
                errors.append(
                    f"strategy version log {relative_path} contains release "
                    f"{release} from major version {parsed[0]}"
                )
            parsed_releases.append(parsed)
            release_versions.append(release)

        if parsed_releases != sorted(parsed_releases) or len(parsed_releases) != len(
            set(parsed_releases)
        ):
            errors.append(
                f"strategy version log {relative_path} releases must be unique "
                "and in ascending order"
            )

        expected_contents = [
            f"- [`{release}`](#{markdown_anchor(release)})"
            for release in release_headings
        ]
        actual_contents = markdown_section_lines(text, "Contents")
        if actual_contents != expected_contents:
            errors.append(
                f"strategy version log {relative_path} contents must link "
                "every release exactly once in heading order"
            )

    if len(release_versions) != len(set(release_versions)):
        errors.append("strategy release headings must be unique across version logs")

    missing_releases = REQUIRED_STRATEGY_RELEASES - set(release_versions)
    if missing_releases:
        errors.append(
            "strategy version history is missing releases "
            f"{sorted(missing_releases)}"
        )

    current = semver_tuple(current_version) if current_version is not None else None
    documented = [
        parsed
        for release in release_versions
        if (parsed := semver_tuple(release)) is not None
    ]
    if current is not None and (not documented or max(documented) != current):
        errors.append(
            "strategy current_version must match the highest documented release"
        )

    return errors, release_versions


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

    all_skill_files = list(ROOT.rglob("SKILL.md"))
    if len(all_skill_files) != len(EXPECTED_SKILLS):
        errors.append(f"expected exactly two SKILL.md files, found {len(all_skill_files)}")

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

    strategy = SKILLS_DIR / "strategy-creator"
    strategy_references = strategy / "references"
    actual_strategy_refs = {
        path.name for path in strategy_references.iterdir() if path.is_file()
    }
    if actual_strategy_refs != EXPECTED_STRATEGY_REFERENCES:
        errors.append(
            "strategy-creator references must be exactly "
            f"{sorted(EXPECTED_STRATEGY_REFERENCES)}"
        )
    strategy_reference_directories = {
        path.name for path in strategy_references.iterdir() if path.is_dir()
    }
    if strategy_reference_directories != {"versions"}:
        errors.append(
            "strategy-creator reference directories must contain only versions"
        )

    strategy_scripts = {
        path.relative_to(strategy / "scripts").as_posix()
        for path in (strategy / "scripts").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if strategy_scripts != EXPECTED_STRATEGY_SCRIPTS:
        errors.append(
            "strategy-creator scripts must be exactly "
            f"{sorted(EXPECTED_STRATEGY_SCRIPTS)}"
        )

    plan_template = strategy / "references" / "plan-template.md"
    version_reference = strategy / "references" / "versioning.md"
    version_directory = strategy / "references" / "versions"
    version_files = {
        path.relative_to(version_directory).as_posix(): path.read_text(
            encoding="utf-8"
        )
        for path in version_directory.rglob("*")
        if path.is_file()
    }
    current_version: str | None = None
    if version_reference.is_file():
        try:
            version_fields = frontmatter(version_reference)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if set(version_fields) != {"current_version"}:
                errors.append(
                    "strategy version reference must declare only current_version"
                )
            current_version = version_fields.get("current_version")
            if current_version is None or STRICT_SEMVER_PATTERN.fullmatch(
                current_version
            ) is None:
                errors.append(
                    "strategy version reference must use strict MAJOR.MINOR.PATCH"
                )

    version_text = (
        version_reference.read_text(encoding="utf-8")
        if version_reference.is_file()
        else ""
    )
    version_errors, _release_versions = validate_strategy_version_history(
        version_text,
        version_files,
        current_version,
    )
    errors.extend(version_errors)

    if plan_template.is_file():
        plan_text = plan_template.read_text(encoding="utf-8")
        try:
            plan_fields = frontmatter(plan_template)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if plan_fields.get("status") != "draft":
                errors.append("strategy plan template must start in draft status")
            if set(plan_fields) != {"status", "contract_version"}:
                errors.append(
                    "strategy plan template must declare status and contract_version"
                )
            plan_version = plan_fields.get("contract_version")
            if plan_version is None or STRICT_SEMVER_PATTERN.fullmatch(
                plan_version
            ) is None:
                errors.append(
                    "strategy plan template contract_version must use strict "
                    "MAJOR.MINOR.PATCH"
                )
            elif current_version is not None and plan_version != current_version:
                errors.append(
                    "strategy plan template contract_version must match the "
                    "strategy version reference"
                )
        missing_sections = REQUIRED_PLAN_SECTIONS - set(plan_text.splitlines())
        if missing_sections:
            errors.append(
                "strategy plan template is missing sections "
                f"{sorted(missing_sections)}"
            )
        actual_plan_section_order = tuple(
            line
            for line in plan_text.splitlines()
            if line in REQUIRED_PLAN_SECTIONS
        )
        if actual_plan_section_order != REQUIRED_PLAN_SECTION_ORDER:
            errors.append(
                "strategy plan template sections must use order "
                f"{list(REQUIRED_PLAN_SECTION_ORDER)}"
            )
        plan_lines = {line.partition(" _")[0] for line in plan_text.splitlines()}
        missing_fields = REQUIRED_PLAIN_LANGUAGE_PLAN_FIELDS - plan_lines
        if missing_fields:
            errors.append(
                "strategy plan template is missing plain-language fields "
                f"{sorted(missing_fields)}"
            )
        missing_target_fields = REQUIRED_TARGET_PLAN_FIELDS - plan_lines
        if missing_target_fields:
            errors.append(
                "strategy plan template is missing AlphaInsider target fields "
                f"{sorted(missing_target_fields)}"
            )
        missing_operation_fields = REQUIRED_OPERATION_PLAN_FIELDS - plan_lines
        if missing_operation_fields:
            errors.append(
                "strategy plan template is missing operation-and-scheduling fields "
                f"{sorted(missing_operation_fields)}"
            )
        obsolete_fields = {
            field for field in REMOVED_PLAN_FIELDS if field in plan_text
        }
        if obsolete_fields:
            errors.append(
                "strategy plan template contains removed fields "
                f"{sorted(obsolete_fields)}"
            )
        obsolete_sections = REMOVED_PLAN_SECTIONS & set(plan_text.splitlines())
        if obsolete_sections:
            errors.append(
                "strategy plan template contains removed sections "
                f"{sorted(obsolete_sections)}"
            )

    strategy_text = (strategy / "SKILL.md").read_text(encoding="utf-8")
    reference_texts = {
        name: (strategy_references / name).read_text(encoding="utf-8")
        for name in EXPECTED_STRATEGY_REFERENCES
    }
    strategy_id_field_references = {
        name
        for name, text in reference_texts.items()
        if "\n- AlphaInsider strategy ID:" in text
    }
    if strategy_id_field_references != {"plan-template.md"}:
        errors.append(
            "only the strategy plan template may define an AlphaInsider strategy ID field"
        )
    long_references_without_contents = {
        name
        for name, text in reference_texts.items()
        if len(text.splitlines()) > 100 and "## Contents" not in text
    }
    if long_references_without_contents:
        errors.append(
            "strategy-creator long references must include contents navigation "
            f"{sorted(long_references_without_contents)}"
        )
    target_text = reference_texts["alphainsider-target.md"]
    cleanup_text = reference_texts["cleanup.md"]
    operation_text = reference_texts["operation-and-scheduling.md"]
    normalized_strategy_text = " ".join(strategy_text.split())
    if len(strategy_text.split()) > STRATEGY_SKILL_MAX_WORDS:
        errors.append(
            "strategy-creator SKILL.md exceeds compact-word limit "
            f"{STRATEGY_SKILL_MAX_WORDS}"
        )
    missing_reference_routes = {
        name
        for name in EXPECTED_STRATEGY_REFERENCES
        if f"references/{name}" not in strategy_text
    }
    if missing_reference_routes:
        errors.append(
            "strategy-creator SKILL.md is missing direct reference routes "
            f"{sorted(missing_reference_routes)}"
        )
    missing_progressive_disclosure = {
        guidance
        for guidance in REQUIRED_PROGRESSIVE_DISCLOSURE_GUIDANCE
        if guidance not in normalized_strategy_text
    }
    if missing_progressive_disclosure:
        errors.append(
            "strategy-creator SKILL.md is missing progressive-disclosure guidance "
            f"{sorted(missing_progressive_disclosure)}"
        )
    permission_block = re.search(
        r"## API-key permission gate.*?```text\n(.*?)\n```",
        target_text,
        re.DOTALL,
    )
    documented_permissions = (
        tuple(permission_block.group(1).splitlines()) if permission_block else ()
    )
    if documented_permissions != REQUIRED_STRATEGY_API_PERMISSIONS:
        errors.append(
            "strategy-creator API-key permission bundle must exactly match "
            f"{list(REQUIRED_STRATEGY_API_PERMISSIONS)}"
        )
    missing_states = {
        state for state in EXPECTED_PLAN_STATES if f"`{state}`" not in strategy_text
    }
    if missing_states:
        errors.append(
            "strategy-creator is missing plan states " f"{sorted(missing_states)}"
        )

    interview_text = reference_texts["interview.md"]
    obsolete_questions = {
        question
        for question in REMOVED_INTERVIEW_QUESTIONS
        if question in interview_text
    }
    if obsolete_questions:
        errors.append(
            "strategy interview contains removed evaluation questions "
            f"{sorted(obsolete_questions)}"
        )
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
    obsolete_interview_phases = {
        phase for phase in REMOVED_INTERVIEW_PHASES if phase in interview_text
    }
    if obsolete_interview_phases:
        errors.append(
            "strategy interview contains removed phases "
            f"{sorted(obsolete_interview_phases)}"
        )
    version_history_text = "\n".join(version_files.values())
    all_reference_text = "\n".join(
        reference_texts[name] for name in sorted(reference_texts)
    )
    manual_text = " ".join(
        (
            f"{strategy_text}\n{all_reference_text}\n{version_history_text}"
        ).split()
    )
    current_contract_text = " ".join(
        (f"{strategy_text}\n{all_reference_text}").split()
    )
    stale_operation_guidance = {
        guidance
        for guidance in REMOVED_CURRENT_OPERATION_GUIDANCE
        if guidance in current_contract_text
    }
    if stale_operation_guidance:
        errors.append(
            "strategy-creator contains obsolete operation guidance "
            f"{sorted(stale_operation_guidance)}"
        )
    vendor_specific_agent_guidance = {
        term
        for term in FORBIDDEN_AGENT_SCHEDULER_VENDOR_TERMS
        if term in f"{operation_text}\n{cleanup_text}"
    }
    if vendor_specific_agent_guidance:
        errors.append(
            "strategy-creator agent scheduling must remain vendor-neutral "
            f"{sorted(vendor_specific_agent_guidance)}"
        )
    stale_target_order_guidance = {
        guidance
        for guidance in REMOVED_TARGET_ORDER_GUIDANCE
        if guidance in manual_text
    }
    if stale_target_order_guidance:
        errors.append(
            "strategy-creator contains obsolete target ordering guidance "
            f"{sorted(stale_target_order_guidance)}"
        )
    stale_separate_confirmation_guidance = {
        guidance
        for guidance in REMOVED_SEPARATE_CONFIRMATION_GUIDANCE
        if guidance in manual_text
    }
    if stale_separate_confirmation_guidance:
        errors.append(
            "strategy-creator contains obsolete creation-confirmation guidance "
            f"{sorted(stale_separate_confirmation_guidance)}"
        )
    stale_post_confirmation_approval_guidance = {
        guidance
        for guidance in REMOVED_POST_CONFIRMATION_APPROVAL_GUIDANCE
        if guidance in manual_text
    }
    if stale_post_confirmation_approval_guidance:
        errors.append(
            "strategy-creator contains obsolete post-confirmation approval guidance "
            f"{sorted(stale_post_confirmation_approval_guidance)}"
        )
    stale_target_deletion_guidance = {
        guidance
        for guidance in REMOVED_TARGET_DELETION_GUIDANCE
        if guidance in current_contract_text
    }
    if stale_target_deletion_guidance:
        errors.append(
            "strategy-creator contains obsolete target-deletion guidance "
            f"{sorted(stale_target_deletion_guidance)}"
        )
    missing_replacement_guidance = {
        guidance
        for guidance in REQUIRED_REPLACEMENT_GUIDANCE
        if guidance not in manual_text
    }
    if missing_replacement_guidance:
        errors.append(
            "strategy-creator is missing replacement guidance "
            f"{sorted(missing_replacement_guidance)}"
        )

    missing_cleanup_guidance = {
        guidance
        for guidance in REQUIRED_CLEANUP_GUIDANCE
        if guidance not in manual_text
    }
    if missing_cleanup_guidance:
        errors.append(
            "strategy-creator is missing cleanup and retirement guidance "
            f"{sorted(missing_cleanup_guidance)}"
        )

    missing_credential_guidance = {
        guidance
        for guidance in REQUIRED_CREDENTIAL_GUIDANCE
        if guidance not in manual_text
    }
    if missing_credential_guidance:
        errors.append(
            "strategy-creator is missing credential setup guidance "
            f"{sorted(missing_credential_guidance)}"
        )
    current_credential_text = " ".join(
        reference_texts[name]
        for name in (
            "alphainsider-target.md",
            "credentials.md",
            "implementation.md",
            "interview.md",
        )
    )
    stale_live_input_guidance = {
        guidance
        for guidance in REMOVED_LIVE_INPUT_CREDENTIAL_GUIDANCE
        if guidance in current_credential_text
    }
    if stale_live_input_guidance:
        errors.append(
            "strategy-creator contains obsolete live-input credential guidance "
            f"{sorted(stale_live_input_guidance)}"
        )

    missing_provisioning_guidance = {
        guidance
        for guidance in REQUIRED_PROVISIONING_GUIDANCE
        if guidance not in manual_text
    }
    if missing_provisioning_guidance:
        errors.append(
            "strategy-creator is missing AlphaInsider provisioning guidance "
            f"{sorted(missing_provisioning_guidance)}"
        )

    missing_single_confirmation_guidance = {
        guidance
        for guidance in REQUIRED_SINGLE_CONFIRMATION_GUIDANCE
        if guidance not in manual_text
    }
    if missing_single_confirmation_guidance:
        errors.append(
            "strategy-creator is missing single-confirmation guidance "
            f"{sorted(missing_single_confirmation_guidance)}"
        )

    missing_local_only_target_guidance = {
        guidance
        for guidance in REQUIRED_LOCAL_ONLY_TARGET_GUIDANCE
        if guidance not in manual_text
    }
    if missing_local_only_target_guidance:
        errors.append(
            "strategy-creator is missing local-only-target guidance "
            f"{sorted(missing_local_only_target_guidance)}"
        )

    missing_grill_protocol_guidance = {
        guidance
        for guidance in REQUIRED_GRILL_PROTOCOL_GUIDANCE
        if guidance not in manual_text
    }
    if missing_grill_protocol_guidance:
        errors.append(
            "strategy-creator is missing grill-interview protocol guidance "
            f"{sorted(missing_grill_protocol_guidance)}"
        )

    missing_operation_guidance = {
        guidance
        for guidance in REQUIRED_OPERATION_GUIDANCE
        if guidance not in manual_text
    }
    if missing_operation_guidance:
        errors.append(
            "strategy-creator is missing operation-and-scheduling guidance "
            f"{sorted(missing_operation_guidance)}"
        )

    missing_startup_guidance = {
        guidance
        for guidance in REQUIRED_STARTUP_GUIDANCE
        if guidance not in manual_text
    }
    if missing_startup_guidance:
        errors.append(
            "strategy-creator is missing generated README startup guidance "
            f"{sorted(missing_startup_guidance)}"
        )

    missing_exposure_guidance = {
        guidance
        for guidance in REQUIRED_EXPOSURE_GUIDANCE
        if guidance not in manual_text
    }
    if missing_exposure_guidance:
        errors.append(
            "strategy-creator is missing portfolio exposure guidance "
            f"{sorted(missing_exposure_guidance)}"
        )

    missing_market_data_guidance = {
        guidance
        for guidance in REQUIRED_MARKET_DATA_GUIDANCE
        if guidance not in manual_text
    }
    if missing_market_data_guidance:
        errors.append(
            "strategy-creator is missing market-data source guidance "
            f"{sorted(missing_market_data_guidance)}"
        )

    missing_version_guidance = {
        guidance
        for guidance in REQUIRED_VERSION_GUIDANCE
        if guidance not in manual_text
    }
    if missing_version_guidance:
        errors.append(
            "strategy-creator is missing versioning guidance "
            f"{sorted(missing_version_guidance)}"
        )

    missing_strategy_version_layout_guidance = {
        guidance
        for guidance in REQUIRED_STRATEGY_VERSION_LAYOUT_GUIDANCE
        if guidance not in agent_guide_text
    }
    if missing_strategy_version_layout_guidance:
        errors.append(
            "AGENTS.md is missing Strategy Creator version-layout guidance "
            f"{sorted(missing_strategy_version_layout_guidance)}"
        )

    update_checker = strategy / "scripts" / "check_for_update.py"
    if update_checker.is_file():
        checker_source = update_checker.read_text(encoding="utf-8")
        missing_checker_source = {
            marker
            for marker in REQUIRED_UPDATE_CHECKER_SOURCE
            if marker not in checker_source
        }
        if missing_checker_source:
            errors.append(
                "strategy update checker is missing required safeguards "
                f"{sorted(missing_checker_source)}"
            )

    env_helper = strategy / "scripts" / "set_env_value.py"
    if env_helper.is_file():
        helper_source = env_helper.read_text(encoding="utf-8")
        required_helper_source = {
            '"--remove",',
            'parser.add_argument("value", nargs="?"',
            'if __name__ != "__main__":',
            "set_env_value.py is CLI-only",
            "Agent-only update or removal",
            "def _remove_env(",
            "def _removed_contents(",
            "def _update_env(",
            "if args.value is not None:",
            "if args.value is None:",
            "_update_env(env_path, args.name, args.value)",
            'action = "Removed" if args.remove else "Updated"',
        }
        missing_helper_source = {
            marker for marker in required_helper_source if marker not in helper_source
        }
        if missing_helper_source:
            errors.append(
                "strategy environment helper is missing CLI-only safeguards "
                f"{sorted(missing_helper_source)}"
            )
        obsolete_helper_source = {
            marker
            for marker in ("getpass", "sys.stdin", "Ready for", "live process-input")
            if marker in helper_source
        }
        if obsolete_helper_source:
            errors.append(
                "strategy environment helper contains obsolete live-input behavior "
                f"{sorted(obsolete_helper_source)}"
            )
        public_helper_functions = re.findall(
            r"^def ([A-Za-z][A-Za-z0-9_]*)\(", helper_source, re.MULTILINE
        )
        if public_helper_functions:
            errors.append(
                "strategy environment helper exposes public Python functions "
                f"{sorted(public_helper_functions)}"
            )
        import_guard_position = helper_source.find('if __name__ != "__main__":')
        first_function_position = helper_source.find("\ndef ")
        if (
            import_guard_position == -1
            or first_function_position == -1
            or import_guard_position > first_function_position
        ):
            errors.append(
                "strategy environment helper must reject imports before defining functions"
            )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme_text.split())
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

    alphainsider = SKILLS_DIR / "alphainsider"
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
    print("validated skills: alphainsider, strategy-creator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
