---
name: alphainsider
description: Route an explicit AlphaInsider skill request to the matching published specialist. Use only when the user runs /alphainsider, says "use the alphainsider skill", "route this with alphainsider", or "which AlphaInsider skill".
---

# AlphaInsider

Version: 0.1.0

## Updates

1. On first interactive use per conversation, inspect this environment's installed
   AlphaInsider versions and read all pages of [public GitHub releases](https://api.github.com/repos/AlphaInsider/skills/releases?per_page=100)
   without authentication. Compare numerically with the highest published stable
   `vX.Y.Z`; ignore drafts, prereleases, bare tags, and Latest. For older/unknown
   copies, show installed/available versions, label unknowns, and pause:
   **Update all** or **Continue**. Share results/choices across skills; recheck
   on request. Skip unattended runs. Continue quietly on automatic lookup failure
   or no releases; explain explicit-check failures.

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

## Route

- Zero matches: say so, list the catalog, and ask which skill.
- Two or more matches: always ask. Do not silently pick.
- One match or a user pick: load that specialist in this turn.

## Load

1. If `npx skills list` shows the specialist installed, follow that installed
   copy's `SKILL.md`, references, and scripts.
2. Otherwise temp-use the full package from GitHub. Never pass `--agent`:

   ```bash
   npx skills@latest use https://github.com/AlphaInsider/skills --skill <name>
   ```

   Parse the support-directory path from stdout and follow that `SKILL.md`.
   Relative scripts and references come from that directory.
3. If temp-use fails, stop and show the persist install command. Do not fetch
   individual GitHub files.

## Persist

Install a specialist only when the user asks. If they do not say global vs
this project, ask and recommend global.

```bash
npx skills@latest add https://github.com/AlphaInsider/skills --skill <name> -g -y
```

Omit `-g` for this project. Let the skills CLI detect agents. After a
successful install, follow the installed copy in this turn.

Do not require any specialist to be preinstalled. Do not install specialists
as a side effect of routing. Never inspect or print existing API keys or
`.env` values.

## References

- [`references/catalog.md`](references/catalog.md) — routable specialists
