---
current_version: 1.0.0
---

# AlphaInsider Versioning

Use one SemVer for this installed wrapper. Versions are strict numeric
`MAJOR.MINOR.PATCH` values with no prerelease or build suffixes.

- Increment major for breaking router behavior.
- Increment minor for a new catalog entry or backward-compatible behavior.
- Increment patch for corrections or documentation-only changes.
- Increment the version for every published change to this skill.
- Do not keep version logs.

The canonical source is
`https://github.com/AlphaInsider/skills/tree/master/skills/alphainsider`.
Run `scripts/check_for_update.py` once at the start of every invocation. It
compares this installed version with the canonical repository and reports only
a newer valid version. The notice is advisory: never run its update command or
ask for permission to run it. Continue with the installed version. If the
check returns no output, continue silently.

```bash
npx skills@latest update alphainsider
```
