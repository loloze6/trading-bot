"""
E037-29: the installed pre-commit hook must match the tracked one.

WHY THIS EXISTS
---------------
`.git/hooks/` is not version-controlled, so the repo keeps a tracked copy at
`strategy-research/tools/hooks/pre-commit` and you install it by hand. That file's
own header warns a *fresh clone* gets no hooks — and misses the case that
actually happened: an **update** to the tracked copy never reaches an existing
installation.

Measured 2026-08-31: the installed hook was 60 lines, the tracked one 89. The
missing gate was the secret scan (`.env`, `venv/`, `*.key`, and credential
values in the staged diff), added 2026-08-15 in `537558ee` after upstream
committed a real `.env` once. It had been absent for over two weeks and nothing
noticed, because nothing compared the two files.

This is the check whose absence made that invisible. It is three lines of logic;
the reason it did not exist is that nobody thought to write it, not that it was
hard.

SCOPING
-------
Skips where there is no `.git/hooks/` (worktrees, archives) rather than
failing — an uninstallable hook is not a defect in those contexts. It also
skips under CI (`CI` env var): a CI checkout via `actions/checkout` creates a
real `.git/` directory with no hooks installed, which is not drift, just how
CI checkouts work — the environment variable is the only reliable signal for
that, since `.git` being a real directory does not distinguish a CI checkout
from a developer's forgotten install. That means CI cannot enforce this: it is
a developer-machine check, which is exactly where the drift happens.

Measured 2026-08-31/2026-09-01: without the CI skip, this test failed on every
run of `fast-tests` from the commit that introduced it onward
(`test_installed_hook_matches_tracked.py:54`, "No pre-commit hook is
installed") -- a false positive, not a real regression, since no CI checkout
has ever had `.git/hooks/pre-commit` installed.

Second false positive, found by Dorian 2026-09-01: a machine that installs
hooks via `core.hooksPath` (his does) has the tracked hook installed and
running green, but this test looked only at the hardcoded `.git/hooks/`
path and reported it missing. Fixed by resolving the installed path through
`git config --get core.hooksPath` when it is set, same as git itself does,
instead of assuming the default location.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

_SR = Path(__file__).resolve().parent.parent
_REPO = _SR.parent

TRACKED = _SR / "tools" / "hooks" / "pre-commit"


def _installed_hooks_dir() -> Path:
    """Where git actually looks for hooks on this machine.

    `core.hooksPath` overrides the default `.git/hooks/` -- resolved the same
    way git resolves it: relative to the repo root if not absolute.
    """
    try:
        result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=_REPO, capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return _REPO / ".git" / "hooks"
    configured = result.stdout.strip()
    if result.returncode != 0 or not configured:
        return _REPO / ".git" / "hooks"
    path = Path(configured)
    return path if path.is_absolute() else _REPO / path


INSTALLED = _installed_hooks_dir() / "pre-commit"


def test_tracked_hook_exists() -> None:
    """The tracked copy is the source of truth; losing it loses the hook for everyone."""
    assert TRACKED.is_file(), (
        f"{TRACKED} is missing. It is the only version-controlled copy of the "
        f"pre-commit hook -- without it a fresh clone has no way to install one."
    )


def test_installed_hook_matches_tracked() -> None:
    if not (_REPO / ".git").is_dir():
        pytest.skip("no .git directory (worktree, archive, or CI checkout)")
    if os.environ.get("CI"):
        pytest.skip("CI checkout: .git/hooks is never populated here, by design")
    if not INSTALLED.exists():
        pytest.fail(
            "No pre-commit hook is installed, so none of its gates run here -- "
            "including the secret scan.\n"
            f"    cp {TRACKED.relative_to(_REPO)} .git/hooks/pre-commit\n"
            "    chmod +x .git/hooks/pre-commit"
        )

    tracked = TRACKED.read_text(encoding="utf-8", errors="replace")
    installed = INSTALLED.read_text(encoding="utf-8", errors="replace")
    if installed == tracked:
        return

    # Be specific about what is missing rather than just "they differ".
    gates = {
        "secret scan": "Secret scan",
        "holdout date gate": "Holdout date gate",
        "test suite": "Running tests before commit",
    }
    missing = [name for name, marker in gates.items()
               if marker in tracked and marker not in installed]

    detail = (f"\nGates present in the tracked hook but NOT running here: "
              f"{', '.join(missing)}." if missing else
              "\nNo named gate is missing, but the files still differ -- the installed "
              "copy is out of date in some other way.")

    pytest.fail(
        f"The installed pre-commit hook does not match the tracked one "
        f"({len(installed.splitlines())} lines installed vs "
        f"{len(tracked.splitlines())} tracked).{detail}\n"
        f"Re-install it:\n"
        f"    cp {TRACKED.relative_to(_REPO)} .git/hooks/pre-commit\n"
        f"    chmod +x .git/hooks/pre-commit\n"
        f"See E-037 FINDINGS.md E037-29."
    )
