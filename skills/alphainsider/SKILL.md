---
name: alphainsider
description: Route an explicit AlphaInsider skill request to the matching published specialist. Use only when the user runs /alphainsider, says "use the alphainsider skill", "route this with alphainsider", or "which AlphaInsider skill".
---

# AlphaInsider

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
