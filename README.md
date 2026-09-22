# AlphaInsider Skills

## Overview

Vendor-neutral skills for AlphaInsider API work and strategy automation.

## Skills

- [`alphainsider`](skills/alphainsider) is the all-in-one AlphaInsider skill. It loads
  the right specialist for API work, strategy creation, backtesting, and automation,
  so you can use all AlphaInsider skills without installing each one separately.
- [`alphainsider-api`](https://api.alphainsider.com/skill.md) is hosted by Mintlify
  and provides current REST, WebSocket, authentication, sizing, and order guidance.
- [`alphainsider-strategy-creator`](skills/alphainsider-strategy-creator) creates and maintains plan-driven strategies,
  backtests, implementations, and native AI automation.

## Install

Ask your agent to install a skill with a prompt below, or download a ZIP for
manual installation.

<a id="coding-assistants-and-terminal-installation"></a>

### Ask your agent to install

Copy the prompt for your skill into your agent. To install the skill for future
conversations, the agent needs access to a supported skill manager or skills
directory. When asked, choose whether to install it for this project or globally
across projects. Installing it on your computer does not add it to a separate web
account.

> [!WARNING]
> If the prompt does not complete the installation, use [Download and Install](#download-and-install)
> to download the skill and install it manually.

For the all-in-one AlphaInsider skill:

```text
Install the latest alphainsider skill from https://github.com/AlphaInsider/skills for use in future conversations. Confirm where it was installed and whether it is ready to use.
```

Invoke it with `/alphainsider`, “use the alphainsider skill,” “route this with
alphainsider,” or “which AlphaInsider skill.”

For the hosted API skill:

```text
Install the latest alphainsider-api skill from https://api.alphainsider.com/skill.md for use in future conversations. Confirm where it was installed and whether it is ready to use.
```

For Strategy Creator:

```text
Install the latest alphainsider-strategy-creator skill from https://github.com/AlphaInsider/skills for use in future conversations. Confirm where it was installed and whether it is ready to use.
```

Strategy Creator reads the hosted API skill when needed, so you can use it
without installing the API skill separately. If you have an older GitHub copy of
the API skill, replace it with the hosted version.

### Download and Install

For Claude, ChatGPT, and Grok (xAI), your account must support skill uploads.
Upload one ZIP per skill through the website's skill manager. Pasting a GitHub
link or attaching files to an ordinary chat does not install a reusable skill.

1. Download the latest [AlphaInsider ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider.zip)
   for the all-in-one skill, or [Strategy Creator ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider-strategy-creator.zip)
   for a dedicated strategy skill. Download both if you want to invoke either skill directly.
2. Upload each ZIP using the steps for your website in the table below. Use the
   downloaded file as is, without extracting or repackaging it.
3. Finish installation and enable the skill. Start a new conversation and name
   the skill in your request.

The links above download the latest release. To use a specific version, open
[GitHub releases](https://github.com/AlphaInsider/skills/releases) and choose the
skill ZIP under that release's **Assets**.

If an older release has no skill ZIPs, or you need an unreleased branch, download
**Source code (zip)** or use **Code → Download ZIP**. Extract the download and open
`skills/`. Compress each skill folder separately with **Compress** in macOS Finder
or **Compress to ZIP file** in Windows File Explorer. Include its `SKILL.md` and
all references and scripts.

Each ZIP must contain one skill folder at the top level:

```text
alphainsider-strategy-creator.zip
└── alphainsider-strategy-creator/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

Use a clean download and keep `.env`, API keys, and strategy projects out of the
archive. Upload the individual skill ZIP, not the entire repository ZIP, the
parent `skills/` folder, or only `SKILL.md`.

| Web client | Upload location |
| --- | --- |
| Claude | **Customize → Skills → + → Create skill → Upload a skill**, then enable it. Code execution and file creation must be enabled. See [Claude's instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude). |
| ChatGPT | **Plugins → Skills → Create → Upload from your computer**. Complete the upload review and installation. Access depends on your workspace; see [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt). |
| Grok (xAI) | Open [Skills](https://grok.com/skills) and use the available skill upload/import flow, then save and enable the skill. See [Grok Skills](https://x.ai/news/grok-skills). |

If you cannot find the upload option, check the site's account and workspace
settings. You can also share this README with an assistant that has web access
and name the skill you want to use. It can follow the
[raw skill links](AGENTS.md#published-skills) for that conversation. Ask it to
confirm which files it loaded and report any missing references or scripts.
You will need to load the skill again in a future conversation.

The API skill is [hosted separately](https://api.alphainsider.com/skill.md). This
repository has no `alphainsider-api` folder. Your assistant can read the hosted
file directly. If your website requires a ZIP, save the file as
`alphainsider-api/SKILL.md` inside a new `alphainsider-api` folder, then compress
and upload that folder. The linked documentation still requires web access.

## Use and update

After installation, try:

```text
Using the alphainsider-strategy-creator skill, help me turn this idea into an automated AlphaInsider paper-trading strategy: [describe your idea].
```

Ask the assistant to confirm it can read `SKILL.md` and the bundled references and
scripts. Installing a skill does not give your assistant execution, persistent
storage, or scheduling access. Strategy Creator checks these before starting
strategy work.

To update a skill you uploaded, download the latest [Strategy Creator ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider-strategy-creator.zip)
or [AlphaInsider ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider.zip)
and replace your installed copy through the website's update/import flow. Enable
the new copy and start a fresh conversation. Uploaded skills do not update
automatically from GitHub. Get API skill updates from its hosted source.

To have your agent update an installed skill, copy the matching prompt:

```text
Update my installed alphainsider skill to the latest version from https://github.com/AlphaInsider/skills. Preserve its current installation scope and report what changed.
```

```text
Update my installed alphainsider-api skill from https://api.alphainsider.com/skill.md. Preserve its current installation scope and report what changed.
```

```text
Update my installed alphainsider-strategy-creator skill to the latest version from https://github.com/AlphaInsider/skills. Preserve its current installation scope and report what changed.
```

## How it works

The [access check](skills/alphainsider-strategy-creator/references/workflow-contracts.md#check-platform-and-automation-access)
verifies execution and persistent file access before project work. Use the host
application's native AI scheduler unless unsupported or the user explicitly requests
external scheduling.

Strategy Creator guides **Define strategy → Backtest → Implement** using
ranked workflow outlines: number only operations that require sequence; use
bullets and sub-bullets for other notes, ranked by importance. Question rounds
present options on consecutive lines, with recommendations. After strategy definition
and backtesting, a summary and standalone next-step question let users backtest, implement on
AlphaInsider, revise, or stop. Required user actions get their own turn; questions
resume after completion. Questions and guardrails reflect actual AI scheduling,
AlphaInsider, and data limits. Backtest planning starts with feasibility and
useful alternatives; users can skip after reviewing limitations. Results include
charts and visuals when possible.

The project's root `plan.md` records decisions, progress, resources, open questions,
workspace/runner binding and access evidence, and the next action. Its flexible
outline supports later chats. Secrets stay in project `.env`; users may paste
new API keys for the non-echoing helper or edit `.env` themselves. Agents never
inspect existing secret values.
Before requesting a key, create missing `.env` and `.env.example` files with an
empty `ALPHAINSIDER_API_KEY=` entry.

Implementation recommends a new public AlphaInsider strategy and offers compatible
owned strategies. Users choose self-healing and notification settings. Trading
decisions can use code, scheduled AI judgment, or both. The skill generates
project-specific code and a runbook; AlphaInsider strategies use simulated funds.

Each scheduled agent runs the program command and evaluates expected outcomes.
Shared exclusivity prevents overlapping runs. On an error, execution blocks
new orders and pauses the scheduler. Enabled self-healing may repair any
implementation issue that preserves the plan's decisions and needs no human
input or new authority. A dry run without orders verifies the fix before a
suitable immediate rerun or resumption for the next scheduled run. Unresolved
or interrupted recovery stays paused for the user. Notifications explain the
issue, automation state, and next step through the selected events and channels.

New schedules activate automatically during setup for the next run, without
another prompt. Access is rechecked for the actual task, alongside agent-controlled
pause/resume, using configuration and documentation; no prior scheduled run is
required. Explicit user pauses or concrete setup failures keep automation
inactive. Local checks and backtests never submit AlphaInsider orders.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and testing, and
[Releases](CONTRIBUTING.md#releases) for the `NEW_RELEASE` workflow.
