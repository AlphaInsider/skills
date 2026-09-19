# AlphaInsider Skills

## Overview

Vendor-neutral skills for AlphaInsider API work and strategy automation.

## Skills

- [`alphainsider`](skills/alphainsider) routes an explicit request to a published specialist.
- [`alphainsider-api`](https://api.alphainsider.com/skill.md) is hosted by Mintlify
  and provides current REST, WebSocket, authentication, sizing, and order guidance.
- [`alphainsider-strategy-creator`](skills/alphainsider-strategy-creator) creates and maintains plan-driven strategies,
  backtests, implementations, and native AI automation.

## Install

### Web clients

For Claude, ChatGPT, and Grok (xAI), upload **one ZIP per skill** through the
website's skill upload/import feature.
Sharing a GitHub link or attaching files to an ordinary chat does not by itself
install a reusable skill. Skill uploads must be available for your account.

1. Open a [GitHub release](https://github.com/AlphaInsider/skills/releases) and
   download `alphainsider-strategy-creator.zip` for strategy work and/or
   `alphainsider.zip` for the optional router from **Assets**. Release notes link
   to these individual skill ZIPs.
2. Upload each downloaded ZIP directly using the website's upload flow below;
   no extraction or recompression is needed.
3. Complete installation and enable the skill.
   Start a new conversation and name the skill in your request.

For an older release without skill ZIPs or an unreleased branch, download
**Source code (zip)** or use **Code → Download ZIP**, extract it, and open `skills/`.
Compress each selected skill folder separately, including `SKILL.md` and all its
references and scripts. Use **Compress** in macOS Finder or **Compress to ZIP file**
in Windows File Explorer.

Each ZIP must contain a single skill folder, for example:

```text
alphainsider-strategy-creator.zip
└── alphainsider-strategy-creator/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

Do not upload the entire repository ZIP, the parent `skills/` folder, or only
`SKILL.md`. Package a clean download; keep `.env`, API keys, and strategy projects
out of skill archives.

| Web client | Upload location |
| --- | --- |
| Claude | **Customize → Skills → + → Create skill → Upload a skill**, then enable it. Code execution and file creation must be enabled. See [Claude's instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude). |
| ChatGPT | **Plugins → Skills → Create → Upload from your computer**. Complete the upload review and installation. Access depends on your workspace; see [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt). |
| Grok (xAI) | Open [Skills](https://grok.com/skills) and use the available skill upload/import flow, then save and enable the skill. See [Grok Skills](https://x.ai/news/grok-skills). |

If the upload control is missing, check the site's account and workspace settings.
For conversation-only use, share this README and name the skill; an assistant with
web access can follow the [raw skill links](AGENTS.md#published-skills). Ask it to
confirm that it loaded the required files and to report any unavailable references
or scripts. This does not create a persistent installation.

The API skill is [hosted separately](https://api.alphainsider.com/skill.md), so there
is no `alphainsider-api` folder in this repository. Give that URL to your assistant.
For a website that requires a ZIP, save the hosted file as `alphainsider-api/SKILL.md`
inside a new `alphainsider-api` folder, then compress and upload that folder. Its
linked documentation still requires web access.

### Coding assistants and terminal installation

Run these commands in a terminal with Node.js/npm available. The installer asks
which supported assistant and installation scope to use. Run from your project
for a project installation, or choose a global installation for reuse across projects.
For manual filesystem installation, copy the complete skill folder into your
assistant's supported skills directory. A local install does not install the skill
in a separate web account.

Install the optional router:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider
```

Invoke it with `/alphainsider`, “use the alphainsider skill,” “route this with
alphainsider,” or “which AlphaInsider skill.”

Install the hosted API specialist:

```bash
npx skills@latest add https://api.alphainsider.com --skill alphainsider-api
```

Install Strategy Creator:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider-strategy-creator
```

Strategy Creator reads the hosted API skill as needed; installing it is optional.
If an older GitHub API skill is installed, replace it with the hosted version.

## Use and update

After installation, try:

```text
Using the alphainsider-strategy-creator skill, help me turn this idea into an automated AlphaInsider paper-trading strategy: [describe your idea].
```

Ask the assistant to confirm it can load `SKILL.md` and the bundled references and
scripts. Installation alone does not provide the execution, persistent storage,
or scheduling access needed for strategy automation; the skill checks these first.

For web uploads, download each installed skill's ZIP from the desired release's
**Assets** and replace its uploaded copy using the website's update/import flow.
Confirm the new copy is enabled and start a fresh conversation. Uploaded copies do
not automatically track GitHub. For terminal or filesystem installations, update
through the same installer or replace the complete skill folder. Refresh the API
skill from its hosted source.

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
