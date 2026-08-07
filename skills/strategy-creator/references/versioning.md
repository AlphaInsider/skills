---
current_version: 1.2.0
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
- Increment the version for every published Strategy Creator change. Record
  each release under its major-version file in `references/versions/`, using
  one `vN.md` file per major version.
- Keep this reference, `references/plan-template.md`, and the highest
  documented release on the same version.

The canonical source is
`https://github.com/AlphaInsider/skills/tree/master/skills/strategy-creator`.
Run `scripts/check_for_update.py` once at the start of every invocation. It
compares this installed version with the canonical repository and reports only
a newer valid version. The notice is advisory: never run its update command or
ask for permission to run it. Continue with the installed version. If the
check returns no output, continue silently.

## Version logs

- [Version 1](versions/v1.md)

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

## Upgrade selection and target audit

For a project older than the installed version, first ask whether to update
the existing plan or replace the strategy. A replacement starts on the
installed version and leaves the outgoing project unchanged. For an update:

1. Follow the **Version logs** links for every major number from the project
   version through the installed version, inclusive. For legacy `0.0.0`, start
   with the first indexed major. Select every documented release greater than
   the project version and less than or equal to the installed version. The
   project version does not need its own release heading; the range alone
   determines the selection.
2. Read only the selected release sections and their verification guidance.
   Process the selected release sections in ascending semantic-version order.
   Audit the project against the installed skill, current plan template, this
   reference, and every selected release increment.
3. Combine all selected increments into one target audit. Show the current and
   target versions and every exact create, modify, and delete path. Explain
   required decisions and verification. Request one explicit approval for that
   inventory. If declined, change nothing. Request renewed approval before
   touching any newly discovered path.
4. For behavior-affecting gaps, return the plan to `draft`, interview only the
   missing decisions, and obtain normal plan confirmation before code edits.
   Require the behavior to conform, but preserve the project's existing code
   structure where practical.
5. Advance `contract_version` only after every selected increment's applicable
   plan, documentation, behavior, and tests conform. Set it directly to the
   installed version; do not write intermediate contract versions. Leave the
   previous version in place after an interrupted or failed upgrade.
