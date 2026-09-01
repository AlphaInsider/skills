# Project Root

Read this reference at Start when resolving the project root. Do not ask
where to store the project. Placement questions use the interactive question
prompt in `interview.md`.

## Contents

- [Invocation directory](#invocation-directory)
- [Unusable location](#unusable-location)
- [Plan recognition](#plan-recognition)
- [Walk-up](#walk-up)
- [Existing strategy](#existing-strategy)
- [Non-strategy software project](#non-strategy-software-project)
- [Child discovery](#child-discovery)
- [New child](#new-child)
- [Rename](#rename)

## Invocation directory

Resolve the project root from the session working directory: the process
current working directory. Do not use the host workspace root or walk to a
git root unless that directory is already selected by the rules below.

A new strategy is a dedicated child folder of that directory. Never write
generated strategy files directly into the invocation directory.

The selected project root may differ from the session working directory. Run
project commands from the project root. Announce the exact project path once
when the root is resolved. Credential and setup helpers use `--project-root`
as specified in `credentials.md`.

## Unusable location

Reject an installed skill directory, unsafe system location, or unusable
path without elaborate denylist checks. Stop and tell the user to relaunch
from a writable user-controlled folder. Do not fall back to `~/Desktop` or
`$HOME`. Do not ask for another parent path.

Accept a normal writable user-controlled location, including beneath the
user's home, as the parent of a new child.

## Plan recognition

Recognize `docs/plan.md` when it has exactly one `# Strategy Plan` title and
YAML frontmatter containing exactly one lifecycle `status` whose value is
`draft`, `confirmed`, `implemented`, or `retired`. Ignore additional
frontmatter fields during recognition and never interpret them. On the next
normal plan write, normalize frontmatter to contain only `status`.

Audit every recognized plan against the current `plan-template.md` headings and
fields. Missing current content is an unresolved decision, not a reason to
reject the plan. Follow `interview.md` to resolve only missing or affected
choices before confirmation. Malformed title, frontmatter, or status is not a
recognized plan.

## Walk-up

If the invocation directory or a nearer ancestor contains a recognized
`docs/plan.md`, use the nearest recognized strategy ancestor as the project
root. Do not keep walking to look for sibling projects or git roots.
Walk-up never selects an installed skill directory or unsafe system path.

## Existing strategy

When the selected root is already a recognized strategy, follow
`interview.md`. Never create a nested strategy. Never create a sibling
from inside this project. A second strategy requires relaunching from the
parent. Replace remains the in-folder new-strategy path.

## Non-strategy software project

Ask only when creating a child would clearly mix a trading project into an
existing non-strategy software project. Stay silent for home, Desktop,
scratch folders, and container folders such as `~/projects`. If it is not
clearly a software project, stay silent and continue.

If asked, recommend not creating a child here. A no answer stops; tell the
user to relaunch from a writable user-controlled folder.

## Child discovery

Scan immediate children only. Do not recurse. Classify each recognized
child as live (`draft`, `confirmed`, or `implemented`) or `retired`. Match
the user prompt against the child folder name plus that plan's Objective,
title, status, and asset class. Never open `.env`. Do not crawl source.

- 0 live children: create.
- 1 live child, and the prompt clearly refers to it or is a generic
  Strategy Creator invoke: reuse that child.
- 1 live child, and the prompt clearly asks for a new, another, or
  different strategy: create a sibling.
- N live children, and exactly one clear match: reuse it.
- N live children, and the prompt is generic or ambiguous: ask which
  child, including create new.
- If unsure, ask; do not guess.

Retired children appear in scans and pickers. Do not auto-reuse a retired
child on a generic invoke: treat that case as 0 live children and create.
A prompt about that retired bot reuses it.

Reuse still follows `interview.md`. Show each picker choice as the folder
name and one-line objective.

## New child

Do not create the folder until Objective is answered. Ask Objective first.
After that answer, slug from the Objective:

- Lowercase ASCII kebab-case `[a-z0-9]+` tokens joined by hyphens.
- Drop filler such as a, an, the, strategy, bot, or trading when enough
  content remains.
- Prefer two to four informative tokens.
- If nothing usable remains, use `strategy`.

If `cwd/<slug>` does not exist, create it, write `docs/plan.md` from
`plan-template.md`, and announce the exact path.

If that path exists and is a recognized strategy, ask whether to continue
it, use the next free `slug-2` or `slug-3` as the recommended choice, or
abort.

If that path exists and is not a strategy, ask only the proposed `-2`
path or abort. Never adopt a junk or occupied folder as a new project
root.

## Rename

Rename only if the user asks. Never auto-rename after the slug is set, for
a clearer objective, or for the AlphaInsider public strategy name. A user
requested rename is a path-changing update: return the plan to `draft`,
inventory the exact path actions, and reconfirm.
