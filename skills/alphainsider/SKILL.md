---
name: alphainsider
description: Route an explicit AlphaInsider skill request to the matching published specialist. Use only when the user runs /alphainsider, says "use the alphainsider skill", "route this with alphainsider", or "which AlphaInsider skill".
---

# AlphaInsider

Version: 1.0.0

## Updates

1. On first interactive use per conversation, inspect installed versions of this
   repository's `alphainsider` and `alphainsider-strategy-creator` skills, and read
   all pages of [public GitHub releases](https://api.github.com/repos/AlphaInsider/skills/releases?per_page=100)
   without authentication. Compare numerically with the highest published stable
   `vX.Y.Z`; ignore drafts, prereleases, bare tags, and Latest. For older/unknown
   copies, show installed/available versions, label unknowns, and pause:
   **Update all** or **Continue**. Share results/choices across skills; recheck
   on request. Skip unattended runs. Continue quietly on automatic lookup failure
   or no releases; explain explicit-check failures. The hosted API skill is
   maintained by Mintlify and is excluded from this GitHub release check.

2. On **Update all**, use available capabilities to update existing older/unknown
   copies from the selected release, preserving installation scope. Keep current/newer
   copies; install no missing skills. Reload updated instructions when supported
   and resume. If unable to update, report outcomes, link the release, and give
   suitable manual instructions; continue with available versions.

Optional facade for published AlphaInsider skills. Specialists stay
independently installable.

## Start

Read [`references/catalog.md`](references/catalog.md). Match the user query to
catalog entries. Do not preload specialist skills.
For web-loaded files, resolve relative links against each fetched file's URL,
retaining the same Git ref (`master` in the links below, or the selected release).

## Route

- Zero matches: say so, list the catalog, and ask which skill.
- Two or more matches: always ask. Do not silently pick.
- One match or a user pick: load that specialist in this turn.

## Load

For API work, read the live [AlphaInsider API skill](https://api.alphainsider.com/skill.md)
and follow its navigation and prerequisite guides. Use this source even if an
older GitHub API skill is installed. If required guidance cannot be fetched,
report the missing source and pause dependent API work.

For Strategy Creator:

1. Use available discovery tools to find an installed specialist, such as
   `npx skills list` when supported. Follow its `SKILL.md`, references, and scripts.
2. Otherwise, if the skills CLI is available, temp-use the full package from GitHub.
   Never pass `--agent`:

   ```bash
   npx skills@latest use https://github.com/AlphaInsider/skills --skill alphainsider-strategy-creator
   ```

   Parse the support-directory path from stdout and follow that `SKILL.md`.
   Relative scripts and references come from that directory.
3. If the package tool is unavailable or temp-use fails, read
   [Strategy Creator](https://raw.githubusercontent.com/AlphaInsider/skills/master/skills/alphainsider-strategy-creator/SKILL.md)
   directly, then its required references. Use raw GitHub file URLs instead of folder pages or the GitHub Raw
   button. Report any required file that cannot be fetched and stop dependent work.

## Persist

Install a specialist only when the user asks, using its source and install
command in the [catalog](references/catalog.md). Never install the API skill
from the GitHub repository. For the skills CLI, if the user does not say global
vs this project, ask and recommend global. Append `-g -y` for global installation
or `-y` for this project; let the CLI detect agents. After a successful install,
load the skill using the source rules above.

For installation through supported skill-file storage, download the complete
package, including linked references and scripts, preserving its directory layout
and Git ref. If persistent installation is unavailable, report that limitation;
describe a web-loaded skill as loaded for this conversation, not installed.

Do not require any specialist to be preinstalled. Do not install specialists
as a side effect of routing. Never inspect or print existing API keys or
`.env` values.

## References

- [`references/catalog.md`](references/catalog.md) — routable specialists
