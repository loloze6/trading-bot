"""
manifest.json's git_sha must say when the tree it ran on was NOT the commit it names.

The defect (measured 2026-08-05, E-012 probe): _get_git_sha() is a bare
`git rev-parse HEAD`, so a run executing edited-but-uncommitted code stamps the
sha of whatever commit HEAD happens to point at. The manifest certifies a commit
LABEL, never the tree that actually produced the numbers -- and a reader
reconciling a result against that commit gets no signal that the two differ.
A `-dirty` suffix is that signal.

Every probe here runs against a THROWAWAY repo built under tmp_path and entered
with monkeypatch.chdir -- _get_git_sha() takes no path argument and reads the
process CWD, so pointing it at the real repo would make the tests depend on the
working state of the branch they are run from.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reporting.run_artifact import _get_git_sha             # noqa: E402

SHA40 = re.compile(r"[0-9a-f]{40}")


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True,
    ).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A one-commit git repo, entered at its root. Returns (path, head_sha).

    Carries a tracked sub/ directory so a probe can enter it: production runs
    from trading-bot/, a tracked SUBDIRECTORY of the repo, never from the root.
    """
    path = tmp_path / "repo"
    (path / "sub").mkdir(parents=True)
    _git(path, "init", "--quiet")
    _git(path, "config", "user.email", "test@example.invalid")
    _git(path, "config", "user.name", "Test")
    _git(path, "config", "commit.gpgsign", "false")
    (path / "tracked.txt").write_text("seed\n")
    (path / "sub" / "subtracked.txt").write_text("seed\n")
    _git(path, "add", "tracked.txt", "sub/subtracked.txt")
    _git(path, "commit", "--quiet", "-m", "seed")
    head = _git(path, "rev-parse", "HEAD").strip()
    assert SHA40.fullmatch(head), head
    monkeypatch.chdir(path)
    return path, head


def test_clean_tree_reports_the_bare_sha(repo):
    _, head = repo
    assert _get_git_sha() == head


def test_modified_tracked_file_reports_the_sha_with_a_dirty_suffix(repo):
    path, head = repo
    (path / "tracked.txt").write_text("edited\n")
    assert _get_git_sha() == f"{head}-dirty"


def test_a_root_file_edit_is_seen_from_a_subdirectory(repo, monkeypatch):
    """The geometry production actually uses.

    `main.py simulate` runs from trading-bot/, a tracked SUBDIRECTORY, and
    nothing in the tree chdir's to the repo root. The status check must keep
    whole-repo scope from there: a check narrowed to the working directory --
    a plausible "only scan our own files" edit -- would report clean while a
    file outside it was modified.
    """
    path, head = repo
    monkeypatch.chdir(path / "sub")
    (path / "tracked.txt").write_text("edited\n")
    assert _get_git_sha() == f"{head}-dirty"


def test_an_untracked_file_alone_does_not_mark_the_tree_dirty(repo):
    """Pins the --untracked-files=no decision so nobody "fixes" it into noise.

    This repo permanently carries untracked results/runs/ evidence directories
    and scratch files. An untracked-inclusive check would stamp EVERY run dirty,
    the suffix would stop discriminating, and readers would learn to ignore it.
    The `sha == head` equality below is what discriminates; the shape check
    documents the intent (a bare 40-hex sha) and is deliberately redundant.
    """
    path, head = repo
    (path / "untracked.txt").write_text("scratch\n")
    sha = _get_git_sha()
    assert SHA40.fullmatch(sha), sha
    assert sha == head


def test_outside_a_repo_the_value_degrades_to_unknown(tmp_path, monkeypatch):
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    # Precondition: git must genuinely fail here. If a parent directory ever
    # carried a .git, this test would otherwise pass for the wrong reason.
    probe = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(plain), capture_output=True, text=True
    )
    assert probe.returncode != 0, probe.stdout

    monkeypatch.chdir(plain)
    assert _get_git_sha() == "unknown"
