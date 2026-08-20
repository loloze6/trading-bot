#!/bin/sh
# setup_hooks.sh — one-time per clone: point Git at the repo's tracked hooks.
#
# WHY THIS EXISTS
#   .git/hooks/ is never cloned. Without this step a fresh clone has NO pre-commit
#   gate: no secret scan, no holdout-date scan. Copying the hook by hand works but
#   drifts — the copy silently goes stale the moment the tracked one changes. Setting
#   core.hooksPath makes the tracked directory itself the live hook path, so a `git
#   pull` updates the gates too.
#
#   core.hooksPath is LOCAL config. It cannot be committed, which is exactly why this
#   script exists rather than a config file. Run it once per clone, per machine.
#
# USAGE
#   sh strategy-research/tools/setup_hooks.sh          # wire it up
#   sh strategy-research/tools/setup_hooks.sh --check  # report status, change nothing
#
# NOTE — this REPLACES .git/hooks as the hook source; anything you keep in there stops
# running. This repo ships only .git/hooks/*.sample, so there is normally nothing to
# lose. If you have a personal hook there, move it into the tracked directory instead.

set -u

HOOKS_DIR="strategy-research/tools/hooks"

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "SETUP FAILED: not inside a git repository." >&2
    exit 1
}
cd "$ROOT" || exit 1

[ -f "$HOOKS_DIR/pre-commit" ] || {
    echo "SETUP FAILED: $HOOKS_DIR/pre-commit not found (wrong repo, or a partial checkout?)." >&2
    exit 1
}

current=$(git config --get core.hooksPath || true)

if [ "${1:-}" = "--check" ]; then
    # Exits NONZERO when anything is not wired, so `--check || setup_hooks.sh` works
    # and CI/onboarding can gate on it. A --check that always exited 0 could report
    # "NOT wired" and still look like success to every caller -- the same
    # silently-passing shape as the non-executable hook this script exists to catch.
    rc=0
    echo "core.hooksPath : ${current:-<unset>}"
    if [ -x "$HOOKS_DIR/pre-commit" ]; then
        echo "hook executable: yes"
    else
        echo "hook executable: NO — git silently ignores non-executable hooks"
        rc=1
    fi
    if [ "$current" = "$HOOKS_DIR" ]; then
        echo "STATUS: wired"
    else
        echo "STATUS: NOT wired — run without --check"
        rc=1
    fi
    exit $rc
fi

# Git ignores a hook that is not executable, and does so without failing the commit.
# The tracked file carries mode 100755, but a checkout with core.fileMode=false, or an
# unzipped rather than cloned tree, can land it non-executable. Fix it rather than
# wiring a path that would quietly do nothing.
if [ ! -x "$HOOKS_DIR/pre-commit" ]; then
    chmod +x "$HOOKS_DIR/pre-commit" 2>/dev/null || {
        echo "SETUP FAILED: $HOOKS_DIR/pre-commit is not executable and chmod failed." >&2
        echo "Git silently ignores non-executable hooks, so wiring it now would be a no-op." >&2
        exit 1
    }
    echo "  fixed: made $HOOKS_DIR/pre-commit executable"
fi

# Relative on purpose: Git resolves it against the worktree root (verified from a
# subdirectory on git 2.43), so it survives moving or renaming the checkout in a way an
# absolute path would not.
git config core.hooksPath "$HOOKS_DIR" || {
    echo "SETUP FAILED: could not set core.hooksPath." >&2
    exit 1
}

echo "Hooks wired: core.hooksPath -> $HOOKS_DIR"
echo "Active on every commit in this clone:"
echo "  - secret scan   (forbidden files + credential values in the staged diff)"
echo "  - holdout gate  (no unregistered dates inside the sealed window)"
echo "Tests are not run here by design; CI runs both suites on every push and PR."
echo "Emergency bypass, if you ever need it: git commit --no-verify"
