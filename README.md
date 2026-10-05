<p align="center">
  <a href="https://alphainsider.com">
    <img src="https://api.alphainsider.com/img/logo.svg" alt="AlphaInsider" width="320">
  </a>
</p>

# AlphaInsider Skills

Give your AI assistant the instructions to work with [AlphaInsider](https://alphainsider.com),
research trading ideas, and build automated trading strategies.

A skill is a reusable set of instructions, references, and optional scripts that
your assistant follows. These skills work within your assistant's tools and
permissions, from answering API questions to creating a strategy project you can
revisit in later conversations.

[Choose a skill](#skills) · [Install](#install) · [Try it](#use-the-skills) · [How it works](#how-it-works)

## Skills

| Skill | What it helps you do |
| --- | --- |
| [**AlphaInsider**](skills/alphainsider) (`alphainsider`) | Start with one entry point. It loads the appropriate specialist for API work or strategy creation, backtesting, and automation. |
| [**Strategy Creator**](skills/alphainsider-strategy-creator) (`alphainsider-strategy-creator`) | Turn an idea into a defined strategy, evaluate it with backtests, and implement and schedule it for AlphaInsider forward testing using simulated funds. Resume or update the project later. |
| [**AlphaInsider API**](https://api.alphainsider.com/skill.md) (`alphainsider-api`) | Work with the REST and WebSocket APIs, including authentication, market data, strategies, orders, positions, and bots. Follow current documentation for requests and trading calculations. |

**Start with `alphainsider` if you want access to everything.** It loads specialists
as needed without requiring separate installation. You can also install a
specialist directly. Strategy Creator reads the hosted API skill when needed.

This repository publishes AlphaInsider and Strategy Creator. The API skill is
[hosted separately](https://api.alphainsider.com/skill.md) and maintained with the
API documentation.

## Install

Use an assistant that can load skills and read online documentation. Installation
for future conversations requires a supported skill manager or skills directory;
availability depends on your application and account.

<a id="coding-assistants-and-terminal-installation"></a>

### Ask your agent to install

Copy one prompt into your assistant. When prompted, choose installation for this
project or globally across projects. A local installation applies to that
assistant environment; a separate web account needs its own installation.

**AlphaInsider — all-in-one:**

```text
Install the latest alphainsider skill from https://github.com/AlphaInsider/skills for use in future conversations. Confirm where it was installed and whether it is ready to use.
```

**Strategy Creator:**

```text
Install the latest alphainsider-strategy-creator skill from https://github.com/AlphaInsider/skills for use in future conversations. Confirm where it was installed and whether it is ready to use.
```

**AlphaInsider API:**

```text
Install the latest alphainsider-api skill from https://api.alphainsider.com/skill.md for use in future conversations. Confirm where it was installed and whether it is ready to use.
```

> [!WARNING]
> If the prompt does not complete installation, use [Download and Install](#download-and-install).
> Reading a link or attaching a ZIP to an ordinary chat does not install a reusable skill.

### Download and Install

If your assistant supports skill uploads:

1. Download the [AlphaInsider ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider.zip)
   or [Strategy Creator ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider-strategy-creator.zip).
   Install both if you want to invoke either directly.
2. Upload each ZIP through your application's skill manager, then finish
   installation and enable it. Use the downloaded file as is.
3. Start a new conversation and ask the assistant to confirm it can load the
   skill and its supporting files.

For a specific version, choose its skill ZIP under **Assets** in
[GitHub releases](https://github.com/AlphaInsider/skills/releases).
See the [installation guide](https://api.alphainsider.com/resources/agent-skill)
for web-client instructions.

<details>
<summary>Manual packaging and the hosted API skill</summary>

If a release has no skill ZIPs, or you need an unreleased branch, download the
repository's source ZIP, extract it, and open `skills/`. Compress the individual
skill folder with its `SKILL.md`, references, and scripts:

```text
alphainsider-strategy-creator.zip
└── alphainsider-strategy-creator/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

Keep `.env`, API keys, and generated projects out of the archive. Upload one skill
folder per ZIP.

For the API skill, save the [hosted file](https://api.alphainsider.com/skill.md)
as `alphainsider-api/SKILL.md`, then compress and upload that folder. Its linked
documentation still requires web access. Use this hosted source for API skill
updates as well.

</details>

If installation is unavailable, an assistant with web access can follow the
[raw skill links](AGENTS.md#published-skills) for the current conversation. Ask it
to confirm which files it loaded and report any missing references or scripts.
You will need to load the skill again in future conversations.

<a id="use-and-update"></a>

## Use the skills

Name the skill and describe what you want to do. With the all-in-one skill:

```text
Use the alphainsider skill to help me turn this idea into an automated AlphaInsider paper-trading strategy: [describe your idea].
```

With the API skill installed directly:

```text
Use the alphainsider-api skill to explain how to retrieve my strategy's positions and display their dollar values correctly.
```

If you installed Strategy Creator directly:

```text
Using the alphainsider-strategy-creator skill, help me define and backtest this paper-trading idea: [describe your idea].
```

You can ask to revise an idea, run another backtest, pause automation, or change
an existing strategy. To resume later, give the assistant your project location
and ask it to continue from `plan.md`.

## How it works

The all-in-one skill matches your request to a specialist and asks you to choose
if the request fits more than one. For Strategy Creator, it uses an installed
copy or loads the published files for the conversation. For API work, it reads
the live hosted skill. Routing does not install additional skills.

The API skill guides the assistant through the current documentation for your
task. Strategy Creator takes you through a longer workflow:

1. **Check the environment.** Verify code execution, persistent file access, and
   scheduling capabilities before starting project work. Files must remain
   readable and writable in later chats and scheduled runs. If required access
   is unavailable or unverified, setup stops until it is resolved.
2. **Define the strategy.** Describe your idea and answer questions about trading
   rules, data, timing, and constraints. The assistant checks feasibility and
   records your decisions in `plan.md`.
3. **Evaluate it.** Choose a backtest, revise the idea, or skip testing after
   reviewing limitations. Results include assumptions, reports, and useful
   charts. Backtests and local checks submit no orders.
4. **Implement and schedule.** The assistant builds the program and operating
   instructions. It verifies API access and helps you select a new or compatible
   existing AlphaInsider strategy.
   You choose the schedule, notifications, and whether to enable automatic recovery.
   Agreed setup activates the schedule for its next run unless you have paused it
   or setup is blocked.
5. **Run and maintain.** Each scheduled run follows the saved plan, executes the
   program, and records its outcome. Errors block new orders and pause
   automation. If enabled, automatic recovery can repair implementation issues
   within your agreed decisions and permissions, verify the fix without orders,
   and resume. Issues that need your input stay paused for your attention.

You choose whether to continue, revise, or save and stop after strategy definition
and backtesting. Trading decisions can use fixed code, scheduled AI judgment, or both.

Your project keeps the plan, code, backtest results, run history, and operating
instructions outside the installed skill. Credentials stay in the project's
`.env`, excluded from version control and reports; agents do not inspect or print
existing secret values. AlphaInsider forward testing requires an account and API
key, which the assistant helps you configure.

> [!IMPORTANT]
> Installing a skill does not provide hosting, persistent storage, or a scheduler.
> Strategy Creator uses your application's native AI scheduling unless unsupported
> or you request an external scheduler. Local execution requires the host and
> necessary application to remain running.

## Update installed skills

Ask your assistant to update the installed copy while preserving its scope:

```text
Update my installed alphainsider skill to the latest version from https://github.com/AlphaInsider/skills. Preserve its current installation scope and report what changed.
```

```text
Update my installed alphainsider-strategy-creator skill to the latest version from https://github.com/AlphaInsider/skills. Preserve its current installation scope and report what changed.
```

```text
Update my installed alphainsider-api skill from https://api.alphainsider.com/skill.md. Preserve its current installation scope and report what changed.
```

For uploaded skills, download a fresh ZIP and replace the installed copy through
your application's update or import flow. Enable it and start a fresh conversation.
Uploaded copies do not update automatically from GitHub. AlphaInsider and Strategy
Creator also check for newer stable releases on first interactive use and offer
to update existing installations; unattended runs skip that check.
