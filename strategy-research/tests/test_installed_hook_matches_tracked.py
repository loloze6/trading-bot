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
Skips where there is no `.git/hooks/` (CI checkouts, worktrees, archives) rather
than failing — an uninstallable hook is not a defect in those contexts. That
means CI cannot enforce this: it is a developer-machine check, which is exactly
where the drift happens.
"""
from __future__ import annotations

from pathlib import Path

import pytest

_SR = Path(__file__).resolve().parent.parent
_REPO = _SR.parent

TRACKED = _SR / "tools" / "hooks" / "pre-commit"
INSTALLED = _REPO / ".git" / "hooks" / "pre-commit"


def test_tracked_hook_exists() -> None:
    """The tracked copy is the source of truth; losing it loses the hook for everyone."""
    assert TRACKED.is_file(), (
        f"{TRACKED} is missing. It is the only version-controlled copy of the "
        f"pre-commit hook -- without it a fresh clone has no way to install one."
    )


def test_installed_hook_matches_tracked() -> None:
    if not (_REPO / ".git").is_dir():
        pytest.skip("no .git directory (worktree, archive, or CI checkout)")
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
