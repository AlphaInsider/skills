---
current_version: 1.1.0
---

# Strategy Creator Versioning

Use one shared version for the installed Strategy Creator skill and its
generated-project contract. Versions are strict numeric `MAJOR.MINOR.PATCH`
values with no prerelease or build suffixes.

## Release policy

- Increment major for breaking requirements or changes that invalidate prior
  strategy decisions.
- Increment minor for backward-compatible new requirements.
- Increment patch for corrections or documentation-only changes that add no
  strategy decisions.
- Increment the version for every published Strategy Creator change. Keep this
  reference and `references/plan-template.md` on the same version.

The canonical source is
`https://github.com/AlphaInsider/skills/tree/master/skills/strategy-creator`.
Run `scripts/check_for_update.py` once at the start of every invocation. It
compares this installed version with the canonical repository and reports only
a newer valid version. The notice is advisory: never run its update command or
ask for permission to run it. Continue with the installed version. If the
check returns no output, continue silently.

## Project recognition

- Recognize a versioned `docs/plan.md` from its valid lifecycle status,
  `# Strategy Plan` title, and strict `contract_version` value. Do not require
  an older version to have the latest template headings before auditing it.
- If `contract_version` is absent, recognize only a plan with the current
  title, lifecycle status, and every section heading from the current plan
  template. Treat that exact legacy shape as `0.0.0`; do not infer versions
  for older shapes.
- If a marker is present but malformed, stop without changing the project.
- Compare the project with the installed version from this reference, never a
  remote version. If the project is newer, stop and show:

  ```bash
  npx skills@latest update alphainsider strategy-creator
  ```

  Tell the user to invoke Strategy Creator again after updating.

## Direct target audit

For a project older than the installed version, first ask whether to update
the existing plan or replace the strategy. A replacement starts on the
installed version and leaves the outgoing project unchanged. For an update:

1. Audit the project directly against the installed skill, current plan
   template, and this reference. Do not replay historical migrations.
2. Show the current and target versions and every exact create, modify, and
   delete path. Explain required decisions and verification. Request one
   explicit approval for that inventory. If declined, change nothing. Request
   renewed approval before touching any newly discovered path.
3. For behavior-affecting gaps, return the plan to `draft`, interview only the
   missing decisions, and obtain normal plan confirmation before code edits.
   Require the behavior to conform, but preserve the project's existing code
   structure where practical.
4. Advance `contract_version` only after the applicable plan, documentation,
   behavior, and tests conform. Leave the previous version in place after an
   interrupted or failed upgrade.

## Version 1.1.0 target

The direct upgrade to `1.1.0` adds the AlphaInsider target-source, creation,
access, description, and synchronization fields to `docs/plan.md`. It also
adds the documented API-permission bundle and remote-description maintenance
rules to attributable `README.md` and `AGENTS.md` files.

For a version-only upgrade, classify the configured target as an existing
strategy, preserve its remote metadata, and do not create a strategy or sync
its description. Remote description synchronization begins only after the
user confirms a behavior plan containing the exact description. The upgrade
alone does not require runtime-code or dependency changes.
