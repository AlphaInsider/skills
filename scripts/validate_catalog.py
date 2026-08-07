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
    "interview.md",
    "plan-template.md",
    "versioning.md",
}
REQUIRED_STRATEGY_RELEASES = {"1.0.0", "1.1.0", "1.2.0"}
EXPECTED_STRATEGY_SCRIPTS = {"check_for_update.py", "set_env_value.py"}
EXPECTED_PLAN_STATES = {"draft", "confirmed", "implemented"}
STRICT_SEMVER_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
)
STRATEGY_VERSION_FILE_PATTERN = re.compile(r"^v([1-9][0-9]*)\.md$")
REQUIRED_PLAN_SECTIONS = {
    "# Strategy Plan",
    "## Objective",
    "## AlphaInsider target",
    "## Strategy behavior",
    "## Data and resources",
    "## Execution and risk",
    "## Backtesting",
    "## Implementation",
    "## Confirmation",
}
REQUIRED_PLAIN_LANGUAGE_PLAN_FIELDS = {
    "- Goal:",
    "- Automatic pause or shutdown conditions and logging:",
    "- Tests to run and expected results:",
}
REQUIRED_TARGET_PLAN_FIELDS = {
    "- Target source:",
    "- Owned-strategy discovery:",
    "- Proposed strategy name:",
    "- Owner starting balance:",
    "- Access eligibility and mode:",
    "- Paid cryptocurrency launch price:",
    "- Core creation fields approval:",
    "- Generated AlphaInsider description:",
    "- Description synchronization:",
}
REMOVED_PLAN_FIELDS = {
    "- Why the strategy could work:",
    "- When results will be reviewed:",
    "- What would show the strategy is working:",
    "- What would show the strategy needs changes or should stop:",
    "- User confirmation:",
    "- Confirmation time:",
}
REMOVED_INTERVIEW_QUESTIONS = {
    "Why do you think this trading idea could work?",
    "After how much time or how many trades should we review the results?",
    "What results would tell you the strategy is working?",
    "What loss or behavior would make you change or stop it?",
}
REQUIRED_REPLACEMENT_GUIDANCE = {
    "every section heading from the current plan template",
    "update the existing plan",
    "replace the trading strategy with a new one",
    "`docs/replacement-plan.md`",
    "does not authorize deletion, plan promotion, or implementation",
    "Show the exact proposed deletion paths",
    "separate explicit approval",
    "Never recursively delete the project root",
    "Never delete `.env`",
    "If the user declines",
    "replace `docs/plan.md` with `docs/replacement-plan.md`",
}
REQUIRED_CREDENTIAL_GUIDANCE = {
    "`scripts/set_env_value.py`",
    "`scripts/alphainsider_request.py`",
    "`scripts/alphainsider_stream.py`",
    "Recommend that the user add the values to `.env` themselves",
    "they may paste the values in chat",
    "the value is visible to the agent",
    "non-echoing prompt",
    "Never pass a credential in a command argument",
    "Do not open `.env` before or after the update",
    "approval to update only those names",
    "use the sibling request helper",
    "--remove ALPHAINSIDER_STRATEGY_ID",
}
REQUIRED_STRATEGY_API_PERMISSIONS = (
    "getUserInfo",
    "getStrategies",
    "getStrategyValues",
    "getUserStrategies",
    "getStrategyPerformance",
    "newStrategy",
    "updateStrategy",
    "deleteStrategy",
    "getStrategySubscriptions",
    "getAccountSubscription",
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
)
REQUIRED_PROVISIONING_GUIDANCE = {
    "https://alphainsider.com/settings/developers",
    "`verifyToken` has no selectable permission",
    "stock REST lookup endpoints require no API-key permission",
    "list only the missing permission names",
    "pause all interview, remote creation, and implementation work",
    "use the verified token's `user_id` with `getUserStrategies`",
    "Never pick the first result or create a duplicate silently",
    "Persist an approved selection",
    "Compare the owned strategy count with `limits.max_strategies`",
    "stop if either eligibility check fails",
    "`getAccountSubscription.level > 0`",
    "`getUserInfo.verified` is true",
    "record public access without an extra access question",
    "Never offer paid stock creation",
    "$10 through $1000",
    "public to `private: false, price: 0`",
    "private to `private: true, price: 0`",
    "Changing any core field invalidates that approval",
    "Do not call `newStrategy` before complete plan confirmation",
    "one to three plain-language sentences",
    "write it only to `ALPHAINSIDER_STRATEGY_ID`",
    "report it once",
    "ask whether to delete this exact strategy",
    "Never infer deletion approval",
    "Only after deletion succeeds",
    "Never remove a default that now refers to another strategy",
    "send the current name and owner `input_value` unchanged",
    "If synchronization fails, leave the plan `confirmed`",
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
    "one decision cycle and continuous operation equally",
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
    "renewed approval before touching any newly discovered path",
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
    "offline tests",
    "language-specific `Start` section",
    "explicit approval",
    "never submits AlphaInsider orders",
    "prefer it for supported current market data",
    "Backtests require credible external history",
    "`contract_version`",
    "npx skills@latest update alphainsider strategy-creator",
    "never installed automatically",
    "verifies its required API-key permissions",
    "discovers owned strategies",
    "syncs the confirmed description",
    "`references/versions/vN.md`",
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
        obsolete_fields = {
            field for field in REMOVED_PLAN_FIELDS if field in plan_text
        }
        if obsolete_fields:
            errors.append(
                "strategy plan template contains removed evaluation fields "
                f"{sorted(obsolete_fields)}"
            )

    strategy_text = (strategy / "SKILL.md").read_text(encoding="utf-8")
    target_text = (
        strategy / "references" / "alphainsider-target.md"
    ).read_text(encoding="utf-8")
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

    interview_text = (
        strategy / "references" / "interview.md"
    ).read_text(encoding="utf-8")
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
    version_history_text = "\n".join(version_files.values())
    manual_text = " ".join(
        (
            f"{strategy_text}\n{target_text}\n{interview_text}\n"
            f"{version_text}\n{version_history_text}"
        ).split()
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
            "def remove_env(",
            "def removed_contents(",
            'action = "Removed" if args.remove else "Updated"',
        }
        missing_helper_source = {
            marker for marker in required_helper_source if marker not in helper_source
        }
        if missing_helper_source:
            errors.append(
                "strategy environment helper is missing safe removal support "
                f"{sorted(missing_helper_source)}"
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
