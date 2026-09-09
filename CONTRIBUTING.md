# Contributing

Add each public skill under `skills/<skill-name>/` with a valid `SKILL.md`.
Keep supporting references one level below the skill and include scripts only
when deterministic behavior is valuable.
Give each rule one canonical owner. Link every reference from `SKILL.md` or a
reachable reference, and explain when to read it instead of repeating it.
Strategy Creator uses ranked workflow outlines: number only operations that
require sequence; use bullets and sub-bullets for other notes, ranked by
importance. Preserve literal user-message and command examples within the
relevant item. Validate structure and section links without freezing plan
fields or heading names.
Keep public skills and documentation agent-vendor agnostic; do not require
vendor-specific metadata or behavior.

When adding a public skill, update `EXPECTED_SKILLS` in
`scripts/validate_catalog.py`, add installation and behavior coverage, and
document its separate and combined installation forms in `README.md`. A new
public specialist must also be added to
`skills/alphainsider/references/catalog.md`. Do not copy source-repository
caches, local plans, generated strategies, virtual environments, IDE files, or
credentials into this catalog.

## Development

Set up the local environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm ci
```

Before opening a change, run:

```bash
python scripts/validate_catalog.py
pytest
npm run skills:list
```

New skills must include realistic tests and must not expose credentials or
perform unsafe external mutations during validation.

## Releases

One version covers the entire skills repository. After the release workflows
are merged into `master`, open **Actions → NEW_RELEASE → Run workflow** on
GitHub, select `master`, and enter a version such as `0.1.1`.

Use `X.Y.Z` without a `v` prefix, leading zeros, prerelease suffix, or build
metadata. The version must be at least the current `package.json` version,
and neither its `vX.Y.Z` tag nor its release may already exist.

The workflow always checks out `master`, synchronizes `package.json`,
`package-lock.json`, and `pyproject.toml`, and commits any version changes
together. It pushes the commit to `master`, then creates tag `vX.Y.Z` at
that exact commit and publishes `Release vX.Y.Z` with generated release
notes as the latest release. It does not publish to npm or PyPI.

Release runs are serialized without cancelling an active run. Existing tags
and releases are never deleted or replaced. If publication fails after the
version commit was pushed, that commit remains; retry the same version only
while neither its tag nor release exists. Unchanged versions do not create
empty commits. If a tag or release exists, choose a new version.

The workflows use the built-in `GITHUB_TOKEN` with `contents: write`; no
additional secret is required. Repository and organization Actions settings,
branch protection, and rulesets must permit this token to push version commits
directly to `master` and create tags and releases. API or push failures stop
the workflow.
