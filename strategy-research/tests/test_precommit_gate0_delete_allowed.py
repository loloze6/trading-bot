"""Tests for gate 0 (secret/venv scan) in strategy-research/tools/hooks/pre-commit.

E-006 unblock (2026-09-09): gate 0's forbidden-file check used to match on staged
PATH alone (`git diff --cached --name-only`), with no diff-filter -- so it blocked
not only adding/modifying a file under venv/ (the real risk the hook's own docstring
names: a commit can make content PERMANENT) but also a pure DELETION of an
already-tracked venv/ file, which cannot create any new permanent history (the old
blob is already permanent in history regardless of this commit). That made
`git rm --cached venv/...` impossible to commit without --no-verify. The fix scopes
the check to `--diff-filter=ACMR` (add/modify/copy/rename), leaving deletions through
gate 0 untouched.

Each test builds a THROWAWAY git repo in tmp_path, installs the tracked hook as its
own .git/hooks/pre-commit, and drives real `git commit` invocations against it.
Nothing touches the real repository, its index, or its history. Gate 1 (the holdout
date gate) is constructed to trivially pass in every repo here so failures are
unambiguously about gate 0.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "strategy-research" / "tools" / "hooks" / "pre-commit"
GATE = REPO_ROOT / "strategy-research" / "tools" / "holdout_date_gate.sh"

SH = shutil.which("sh") or shutil.which("bash")

pytestmark = pytest.mark.skipif(
    SH is None or not HOOK.exists() or not GATE.exists(),
    reason="POSIX sh, the tracked pre-commit hook, or holdout_date_gate.sh unavailable",
)


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=check,
    )


def _gate_self_count() -> int:
    """Holdout-date lines in the gate's own source (mirrors test_holdout_date_gate.py).

    Computed rather than hardcoded so this test never drifts if the gate script's
    comments change.
    """
    pat = re.compile(r"2026-0[1-6]-[0-3][0-9]")
    authorship = re.compile(
        r'"(created_utc|timestamp|updated_at|generated_at|generated_utc'
        r'|decision_timestamp|analysis_timestamp)"\s*:'
        r"|^\s*(timestamp|created_utc|updated_at|generated_at|generated_utc|review_date"
        r"|recommendation_date|decision_timestamp|analysis_timestamp)\s*:"
    )
    n = 0
    for line in GATE.read_text(encoding="utf-8").splitlines():
        if pat.search(line) and not authorship.search(line):
            n += 1
    return n


def _make_repo_with_hook(tmp_path: Path, name: str, baseline_files: dict) -> Path:
    """Build a repo with the tracked pre-commit hook installed, after a clean
    baseline commit (made BEFORE the hook exists, so a baseline that includes a
    tracked venv/ file is never itself subject to gate 0)."""
    repo = tmp_path / name
    (repo / "strategy-research" / "config").mkdir(parents=True)
    (repo / "strategy-research" / "tools").mkdir(parents=True)

    # Gate 1 must trivially pass here so every assertion below is about gate 0 only.
    shutil.copy(GATE, repo / "strategy-research" / "tools" / "holdout_date_gate.sh")
    gate_entry = "strategy-research/tools/holdout_date_gate.sh\t%d\n" % _gate_self_count()
    (repo / "strategy-research" / "config" / "holdout_gate_exemptions.txt").write_text(
        "# test registry\n" + gate_entry, encoding="utf-8"
    )

    for rel, content in baseline_files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "baseline (hook not installed yet)")

    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    dest = hooks_dir / "pre-commit"
    shutil.copy(HOOK, dest)  # byte-for-byte copy: preserves LF line endings
    os.chmod(dest, 0o755)

    return repo


def test_new_file_under_venv_is_still_blocked(tmp_path):
    """Adding a NEW file under venv/ must still be blocked by gate 0 (unchanged)."""
    repo = _make_repo_with_hook(
        tmp_path, "add_case", {"README.md": "hello\n", "venv/dummy.txt": "junk\n"}
    )

    (repo / "venv" / "newsecret.txt").write_text("shouldnt be here\n", encoding="utf-8")
    _git(repo, "add", "-A")
    r = _git(repo, "commit", "-q", "-m", "add venv file", check=False)
    out = r.stdout + r.stderr

    assert r.returncode != 0, out
    assert "(secrets/venv policy)" in out, out


def test_deleting_tracked_venv_file_passes_gate0(tmp_path):
    """Deleting an already-tracked venv/ file must NOT trip gate 0's venv block.

    Scoped to gate 0 specifically (per the fix's intent): the repo here is built so
    gate 1 trivially passes too, so this asserts the commit succeeds end-to-end, not
    merely that gate 0's message is absent.
    """
    repo = _make_repo_with_hook(
        tmp_path, "delete_case", {"README.md": "hello\n", "venv/dummy.txt": "junk\n"}
    )

    _git(repo, "rm", "-q", "venv/dummy.txt")
    r = _git(repo, "commit", "-q", "-m", "untrack venv file", check=False)
    out = r.stdout + r.stderr

    assert "(secrets/venv policy)" not in out, out
    assert r.returncode == 0, out
