"""Tests for strategy-research/tools/holdout_date_gate.sh.

The gate is the mechanical guard behind campaign_data_policy.yaml:holdout_range. Its
value depends entirely on it failing CLOSED, so the cases that matter most here are the
ones where the scan cannot run: a gate that silently passes when its scanner is broken
is worse than no gate, because it manufactures false confidence in every commit after it.

Each test builds a THROWAWAY git repo in tmp_path and points the gate at it. Nothing
touches the real repository or its index.
"""

import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = REPO_ROOT / "strategy-research" / "tools" / "holdout_date_gate.sh"

# The gate is /bin/sh; on Windows that is Git's bundled sh.exe.
SH = shutil.which("sh") or shutil.which("bash")

pytestmark = pytest.mark.skipif(
    SH is None or not GATE.exists(),
    reason="POSIX sh or holdout_date_gate.sh unavailable",
)


def _git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    )


def _gate_self_count():
    """How many holdout-date lines the gate's own source carries.

    The gate documents and matches the sealed window, so its source is necessarily a
    hit against itself. In the real repo it is a registry entry; here it is computed so
    the fixture never drifts when the script's comments are edited.
    """
    import re

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


def _make_repo(tmp_path, files, registry_lines=""):
    """Build a git repo with `files` staged, plus the gate + its exemption registry."""
    repo = tmp_path / "repo"
    (repo / "strategy-research" / "config").mkdir(parents=True)
    (repo / "strategy-research" / "tools").mkdir(parents=True)

    shutil.copy(GATE, repo / "strategy-research" / "tools" / "holdout_date_gate.sh")
    gate_entry = (
        "strategy-research/tools/holdout_date_gate.sh\t%d\n" % _gate_self_count()
    )
    (repo / "strategy-research" / "config" / "holdout_gate_exemptions.txt").write_text(
        "# test registry\n" + gate_entry + registry_lines, encoding="utf-8"
    )

    for rel, content in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    _git(repo, "add", "-A")
    return repo


def _run_gate(repo, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [SH, "strategy-research/tools/holdout_date_gate.sh"],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
    )


# --------------------------------------------------------------------------- clean


def test_clean_index_passes(tmp_path):
    """No holdout dates anywhere -> exit 0, and the examined count is non-zero.

    The count assertion is the point: 'no hits' is only meaningful if files were
    actually read.
    """
    repo = _make_repo(
        tmp_path,
        {
            "data/bars.csv": "ts,open\n2025-12-31 23:00:00,100\n",
            "docs/notes.md": "Walk-forward ends 2025-12-31.\n",
        },
    )
    r = _run_gate(repo)
    out = r.stdout + r.stderr

    assert r.returncode == 0, out
    assert "PASS" in out
    assert "files examined:" in out
    examined = int(out.split("files examined:")[1].split()[0])
    assert examined > 0


# ----------------------------------------------------------------------------- hit


def test_holdout_date_in_data_file_blocks(tmp_path):
    """A bar timestamp inside the seal blocks the commit and names file and line.

    This reproduces the exact shape of the contamination dispatch W5 quarantined:
    a bars.csv whose rows cross 2026-01-01.
    """
    repo = _make_repo(
        tmp_path,
        {
            "results/bars.csv": "ts,open\n2025-12-31 23:00:00,100\n2026-01-01 00:00:00,101\n"
        },
    )
    r = _run_gate(repo)
    out = r.stdout + r.stderr

    assert r.returncode == 1, out
    assert "COMMIT BLOCKED" in out
    assert "results/bars.csv" in out  # names the file
    assert "2026-01-01" in out  # names the offending line


def test_boundary_dates(tmp_path):
    """2026-06-30 is sealed and blocks; 2026-07-01 is outside and passes.

    Off-by-one at the closing edge is the likeliest way this gate would silently
    under-enforce, so it is asserted rather than assumed.
    """
    blocked = _make_repo(tmp_path / "a", {"d.csv": "ts\n2026-06-30 23:00:00\n"})
    assert _run_gate(blocked).returncode == 1

    allowed = _make_repo(tmp_path / "b", {"d.csv": "ts\n2026-07-01 00:00:00\n"})
    r = _run_gate(allowed)
    assert r.returncode == 0, r.stdout + r.stderr


def test_authorship_timestamp_is_not_a_hit(tmp_path):
    """`created_utc` inside the window is provenance, not market data -> passes.

    Without this carve-out the gate would flag ~99% of the repo's artifacts, since the
    campaign was authored during 2026 H1.
    """
    repo = _make_repo(
        tmp_path,
        {"run/manifest.json": '{\n  "created_utc": "2026-03-14T10:00:00Z"\n}\n'},
    )
    r = _run_gate(repo)
    assert r.returncode == 0, r.stdout + r.stderr


def test_declared_range_is_still_a_hit(tmp_path):
    """A manifest's declared data range is market data even in a metadata file.

    Guards against the authorship carve-out being over-applied to whole files.
    """
    repo = _make_repo(
        tmp_path,
        {
            "run/manifest.json": (
                '{\n  "created_utc": "2026-03-14T10:00:00Z",\n'
                '  "data": {"start": "2025-12-01", "end": "2026-01-01 23:00:00"}\n}\n'
            )
        },
    )
    r = _run_gate(repo)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "run/manifest.json" in r.stdout + r.stderr


# ------------------------------------------------------------------- registry logic


def test_registered_file_passes_at_its_count(tmp_path):
    repo = _make_repo(
        tmp_path,
        {"docs/policy.md": "holdout is 2026-01-01 to 2026-06-30\n"},
        registry_lines="docs/policy.md\t1\n",
    )
    r = _run_gate(repo)
    assert r.returncode == 0, r.stdout + r.stderr


def test_registered_file_blocks_when_it_gains_a_line(tmp_path):
    """The exemption is pinned to the audited line count, not to the filename."""
    repo = _make_repo(
        tmp_path,
        {
            "docs/policy.md": "holdout is 2026-01-01 to 2026-06-30\nand also 2026-02-05\n"
        },
        registry_lines="docs/policy.md\t1\n",
    )
    r = _run_gate(repo)
    out = r.stdout + r.stderr
    assert r.returncode == 1, out
    assert "EXCEEDS" in out


# ------------------------------------------------------- scanner unavailable / broken


def test_scanner_unavailable_blocks(tmp_path):
    """Missing scanner binary -> FAIL, never pass. Deny by default."""
    repo = _make_repo(tmp_path, {"docs/clean.md": "nothing here\n"})
    r = _run_gate(repo, {"HOLDOUT_GATE_GREP": "/nonexistent/grep"})
    out = r.stdout + r.stderr

    assert r.returncode == 1, out
    assert "self-test" in out
    assert "BLOCKED" in out


def test_permissive_stub_scanner_blocks(tmp_path):
    """A scanner that matches nothing must fail the POSITIVE control, not report clean.

    This is the attack the self-test exists to stop: substituting a scanner that always
    says 'no hits' would otherwise turn the gate into a rubber stamp.
    """
    repo = _make_repo(tmp_path, {"results/bars.csv": "ts\n2026-01-01 00:00:00\n"})
    stub = tmp_path / "bin" / "falsegrep"
    stub.parent.mkdir(parents=True, exist_ok=True)
    stub.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")  # 'never matches'
    stub.chmod(0o755)

    r = _run_gate(repo, {"HOLDOUT_GATE_GREP": str(stub)})
    out = r.stdout + r.stderr
    assert r.returncode == 1, out
    assert "POSITIVE CONTROL FAILED" in out


def test_missing_registry_blocks(tmp_path):
    """Without the registry the gate cannot tell audited from unreviewed -> FAIL."""
    repo = _make_repo(tmp_path, {"docs/clean.md": "nothing here\n"})
    (repo / "strategy-research" / "config" / "holdout_gate_exemptions.txt").unlink()
    _git(repo, "add", "-A")

    r = _run_gate(repo)
    out = r.stdout + r.stderr
    assert r.returncode == 1, out
    assert "registry" in out.lower()


def test_self_test_only_mode(tmp_path):
    repo = _make_repo(tmp_path, {"docs/clean.md": "x\n"})
    r = subprocess.run(
        [SH, "strategy-research/tools/holdout_date_gate.sh", "--self-test-only"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    out = r.stdout + r.stderr
    assert r.returncode == 0, out
    assert "self-test: PASS" in out
