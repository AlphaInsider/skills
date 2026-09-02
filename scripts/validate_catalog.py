#!/usr/bin/env python3
"""Validate the public AlphaInsider skill catalog."""

from __future__ import annotations

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
    "alphainsider-target.md",
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
STRATEGY_SKILL_MAX_WORDS = 1100
REQUIRED_PLAN_SECTION_ORDER = (
    "# Strategy Plan",
    "## Strategy plan",
    "## Backtesting plan",
    "## Implementation plan",
    "## Current status",
)
REQUIRED_PLAN_FIELDS = {
    "- Goal:",
    "- Strict asset class:",
    "- Decision mode:",
    "- Maximum strategy leverage:",
    "- User choice:",
    "- Benchmark:",
    "- Metrics and charts:",
    "- Plan-conformance checks:",
    "- AlphaInsider strategy ID:",
    "- Native AI scheduler provider and task identity:",
    "- Self-healing:",
    "- Notifications:",
    "- Future plan-conforming paper-order authority:",
    "- Phase:",
    "- Plan agreement:",
    "- Highest completed outcome:",
    "- Automation state:",
    "- Automation state reason:",
    "- Last completed step:",
    "- Next step:",
    "- Waiting for:",
    "- Open questions:",
    "- Last updated:",
}
REQUIRED_STATUS_VALUES = {
    "Interviewing",
    "Building backtest",
    "Reviewing results",
    "Building implementation",
    "Configuring automation",
    "Complete",
    "Draft",
    "Agreed",
    "None",
    "Plan",
    "Backtest",
    "Automated strategy",
    "Not configured",
    "Active",
    "Paused",
}
REQUIRED_INTERVIEW_PHASE_ORDER = (
    "## Stage 1: High-level strategy",
    "## Stage 2: Backtest choice and results",
    "## Stage 3: AlphaInsider and automation",
    "## Completion",
)
REQUIRED_STRATEGY_SKILL_GUIDANCE = {
    "`plan.md` is the project's readable source of truth",
    "one strict `stock` or `cryptocurrency` type",
    "Use only the platform's native AI automation or scheduler",
    "Poor performance never makes a plan-conforming run unhealthy",
    "Use only create, resume, update, and explicit deletion paths",
    "Select the safest persistent location without asking the user",
    "Build and pass offline, order-free checks before creating a new target",
    "When `alphainsider-api` is installed, read its `SKILL.md`",
    "Do not preload every reference",
}
REQUIRED_STRATEGY_CONTRACT_GUIDANCE = {
    "ASD-STE100-style technical English",
    "Do not invoke another grilling or interview skill",
    "Never leave the user to ask what happens next",
    "👉 **Action — Short title:**",
    "`⚠️ Warning — No Action Required`",
    "`🛠️ Self-Healed — No Action Required`",
    "`🚨 Error — Action Required`",
    "The location must outlive this chat",
    "`runtime/runbook.md`",
    "is not a health criterion",
    "`$100,000`",
    "supports up to `2×`",
    "Recommend `1×`",
    "scheduler **Run now**",
    "A dry run is available only through an explicit chat request",
    "Missed runs do not catch up",
    "Stop when no meaningful progress remains",
    "30 minutes have elapsed",
    "A notification failure never pauses trading by itself",
    "Use only create, resume, update, and explicit deletion paths",
    "For full deletion, remove the entire selected project and leave no tombstone",
    "https://alphainsider.com/resources#automating-trades",
}
REQUIRED_CORE_LAYOUT = {
    "plan.md",
    ".env",
    ".env.example",
    ".gitignore",
    "README.md",
    "AGENTS.md",
    "strategy/",
    "backtest/",
    "runtime/",
    "tests/",
}
OBSOLETE_STRATEGY_PATHS = {
    "references/cleanup.md",
    "references/operation-and-scheduling.md",
    "references/release.md",
    "docs/replacement-plan.md",
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
README_MAX_WORDS = 650
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
    "paper-trading",
    "code-led, agent-led, or hybrid",
    "backtest",
    "Performance",
    "**AI Agent**",
    "`$100,000`",
    "`1×`",
    "`2×`",
    "self-healing",
    "30 minutes",
    "chat dry run",
    "Explicit deletion",
    "resources#automating-trades",
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


def catalog_specialists(text: str) -> list[str]:
    """Return routable specialist names from catalog headings."""
    return CATALOG_HEADING_PATTERN.findall(text)


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
    normalized_strategy_text = " ".join(strategy_text.split())
    normalized_contract_text = " ".join(
        f"{strategy_text}\n{all_reference_text}".split()
    )

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

    missing_skill_guidance = {
        item
        for item in REQUIRED_STRATEGY_SKILL_GUIDANCE
        if item not in normalized_strategy_text
    }
    if missing_skill_guidance:
        errors.append(
            "strategy-creator SKILL.md is missing core guidance "
            f"{sorted(missing_skill_guidance)}"
        )

    missing_contract_guidance = {
        item
        for item in REQUIRED_STRATEGY_CONTRACT_GUIDANCE
        if item not in normalized_contract_text
    }
    if missing_contract_guidance:
        errors.append(
            "strategy-creator references are missing agreed behavior "
            f"{sorted(missing_contract_guidance)}"
        )

    stale_routes = {
        route for route in OBSOLETE_STRATEGY_PATHS if route in strategy_text
    }
    if stale_routes:
        errors.append(
            "strategy-creator SKILL.md routes to obsolete lifecycle material "
            f"{sorted(stale_routes)}"
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

    missing_plan_fields = {
        field
        for field in REQUIRED_PLAN_FIELDS
        if not any(line.startswith(field) for line in plan_text.splitlines())
    }
    if missing_plan_fields:
        errors.append(
            "strategy plan template is missing fields "
            f"{sorted(missing_plan_fields)}"
        )

    missing_status_values = {
        value for value in REQUIRED_STATUS_VALUES if value not in plan_text
    }
    if missing_status_values:
        errors.append(
            "strategy plan template is missing status choices "
            f"{sorted(missing_status_values)}"
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
