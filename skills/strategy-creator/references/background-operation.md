# Background Operation

Use this phase after strategy design and resource selection and before
AlphaInsider forward-test setup. It plans only the continuous command; a
one-cycle command always remains foreground-only.

## Contents

- [Interview branch](#interview-branch)
- [Collision and running-state checks](#collision-and-running-state-checks)
- [Generated manager behavior](#generated-manager-behavior)
- [Installation and lifecycle](#installation-and-lifecycle)
- [Generated project guidance](#generated-project-guidance)

## Interview branch

Always ask whether the user wants the continuous strategy to run in the
background. Record `foreground only` and normalize every dependent field as
not applicable when they decline.

When they accept:

1. Detect the host and available user-level managers instead of asking the
   user for system facts. On Linux, offer systemd only when the user manager is
   usable. On macOS, offer launchd. Offer tmux only when it is installed. Never
   install a dependency, request sudo, configure a system service or systemd
   lingering, or offer Windows support.
2. Ask the user to select from the usable managers. If none is usable, resolve
   the gap before plan confirmation by having the user select foreground-only
   operation or make a supported manager available.
3. Derive a stable identifier from the project-root directory name: lowercase
   ASCII letters, digits, and hyphens, with other runs collapsed to one hyphen. Use
   `alphainsider-<slug>.service` for systemd,
   `com.alphainsider.strategy.<slug>` for a launchd label and plist name, and
   `alphainsider-<slug>` for a tmux session. Ask for a safe identifier only if
   normalization is empty or a collision cannot otherwise be resolved.
4. For systemd or launchd, ask whether the definition remains disabled or
   starts at the next user login. Explain that login autostart can submit paper
   orders without another prompt. tmux is manual-only and has no autostart.
5. Offer manual failure recovery for every manager. Only systemd may offer
   bounded on-failure restart; when selected, collect a positive restart delay,
   maximum failure count, and evaluation window. Do not represent launchd
   throttling or tmux as bounded restart.
6. Ask whether management instructions expose manager-native output, rotating
   project logs, or both. Record project-relative log paths and any applicable
   size, backup-count, or retention decisions. For native output, use journald
   for systemd, configured standard-output/error paths for launchd, and tmux
   scrollback/capture commands. State when a selected native facility does not
   provide automatic rotation.

Record the capability check, manager, identifier, host definition path,
autostart, restart, log exposure, and installation state. These are plan
decisions, never credentials.

## Collision and running-state checks

Before confirmation, inspect only path existence and manager-reported active
state; never print environment values or secrets from a definition.

- Update a definition only when the current plan and project documentation
  attribute it to this strategy.
- For an unrelated inactive definition, explain the exact overwrite and
  consequences during the interview and record the user's choice in the draft.
  Final complete-plan confirmation authorizes that recorded overwrite.
- Never overwrite an active unrelated definition. Choose a unique identifier
  and record it before final confirmation.
- When a runtime-affecting update finds this strategy's attributable service
  running, disclose the exact stop and autostart-disable actions in the updated
  plan. Reconfirmation authorizes those actions before file changes. Never
  restart it after the update. Leave it stopped, report that prominently, and
  provide the user-run command that starts it and restores planned autostart.

Final replacement-plan confirmation covers the recorded stop, disable, and
removal of only the outgoing strategy's attributable definition. It never
covers another strategy or service.

## Generated manager behavior

Generate no project-local manager wrapper or service template. The exact
selected user-level definition is the only permitted write outside the project
root. Resolve absolute project and executable paths only while rendering that
host definition; keep the plan, project documentation, runtime state, and log
paths project-relative. The strategy process must load its project `.env`;
never copy credentials into a unit, plist, command argument, or tmux command.

### systemd

Install only `~/.config/systemd/user/<identifier>`. Use the project root as
`WorkingDirectory` and the exact continuous executable and arguments as
`ExecStart`. Use `Restart=no` for manual recovery. For bounded recovery, use
`Restart=on-failure` and map the confirmed delay, maximum failures, and window
to `RestartSec`, `StartLimitBurst`, and `StartLimitIntervalSec`.

After writing, run the user-manager reload and enable the unit only when login
autostart was confirmed; never use `--now`. Verify the definition is valid and
inactive. Documentation must use `systemctl --user` for start, stop, restart,
status, enable, disable, and uninstall, and `journalctl --user -u` for native
logs. When planned autostart must be restored after an update, the documented
resume command uses `enable --now`; otherwise it uses `start`.

### launchd

Install only `~/Library/LaunchAgents/<identifier>.plist`. Set the label,
absolute continuous-program arguments, working directory, confirmed
`RunAtLoad` value, and selected output paths. Keep `KeepAlive` false because
finite bounded restart is unsupported. Validate the rendered plist before
installation. Do not bootstrap, load, kickstart, or otherwise start it during
build or verification.

Documentation must provide `launchctl` commands for bootstrap/start, bootout,
restart, status, enable, disable, and uninstall plus commands for the selected
logs. A resume command after an update must re-enable the label when planned
autostart was disabled for the update.

### tmux

Install no host definition. Document the exact detached `tmux new-session`
command using the selected session name and continuous command, plus status,
attach, capture/log, restart, stop, and cleanup commands. Do not offer login
autostart or automatic process restart. Treat successful capability and
documentation verification as completion of the background setup.

## Installation and lifecycle

Complete plan confirmation is the sole authorization to install a new native
definition, but installation occurs only after a ready target is provisioned,
the local build and offline checks pass, and the remote description is
synchronized. Never start a new or replacement strategy. If login autostart is
enabled, state that the service can start at a later login.

Do not request another approval during installation. If the path, active state,
or required action differs from the confirmed inventory, return the plan to
`draft`, resolve that affected decision, and obtain one new complete-plan
confirmation before continuing.

For a deferred target, retain the normalized background decisions but install
nothing and keep every operational and background-management command
unavailable. When target setup resumes, include background installation in the
fully reconfirmed plan.

A required native installation failure leaves the plan `confirmed`, never
`implemented`, and the service stopped. If the current run created the remote
target, apply the confirmed failed-current-run cleanup policy. Set a ready
background-enabled
plan to `implemented` only after the exact native definition is installed and
verified inactive, or after the tmux instructions and capability are verified.
If an update fails after stopping an existing service, leave the plan
`confirmed` and the service stopped; never resume stale or partially updated
code.

## Generated project guidance

The generated `README.md` must identify the selected manager and definition or
session name and provide copy-paste install, start, stop, restart where
supported, status, log, autostart enable/disable, and uninstall instructions.
Warn immediately before the start command that it can submit paper orders
without another prompt. Explain manager limitations and how moving the project
requires reinstalling a native definition.

The generated `AGENTS.md` must preserve the plan fields, credential boundary,
host-only definition exception, collision rules, installation ordering, and
no-automatic-start and single-final-confirmation rules. It must require
runtime-affecting updates to stop and disable an attributable running service
after reconfirmation, never restart it, and report the stopped state and exact
user-run resume command.
