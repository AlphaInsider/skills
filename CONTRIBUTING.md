# Contributing

Add each public skill under `skills/<skill-name>/` with a valid `SKILL.md`.
Keep supporting references one level below the skill and include scripts only
when deterministic behavior is valuable.
Keep public skills and documentation agent-vendor agnostic; do not require
vendor-specific metadata or behavior.

When adding a public skill, update `EXPECTED_SKILLS` in
`scripts/validate_catalog.py`, add installation and behavior coverage, and
document its separate and combined installation forms in `README.md`. A new
public specialist must also be added to
`skills/alphainsider/references/catalog.md`. Do not copy source-repository
caches, local plans, generated strategies, virtual environments, IDE files, or
credentials into this catalog.

Before opening a change, run:

```bash
python scripts/validate_catalog.py
pytest
npm run skills:list
```

New skills must include realistic tests and must not expose credentials or
perform unsafe external mutations during validation.
