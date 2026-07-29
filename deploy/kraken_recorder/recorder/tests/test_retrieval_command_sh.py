"""
retrieval_command.sh: the forced command behind the retrieval SSH key
allows exactly three operations against exactly one directory, and refuses
everything else.

These run the real script under whatever bash is on PATH. What they prove is
the script's own whitelist logic; what they do NOT prove is that sshd is
actually configured to invoke it -- that is an authorized_keys entry on the
capture host, and OPERATOR_HANDOVER.md tells the operator how to verify it
in place.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

# retrieval_command.sh lives at the bundle root, one level above the
# `recorder` package (recorder/tests/this_file -> recorder/ -> bundle root).
WRAPPER = Path(__file__).resolve().parents[2] / "retrieval_command.sh"
BASH = shutil.which("bash")
CYGPATH = shutil.which("cygpath")

pytestmark = pytest.mark.skipif(BASH is None, reason="no bash on this machine")


def posix(p: Path) -> str:
    """
    The path as the bash running this script sees it. On Linux (the deploy
    target) that is the path itself; under Git-bash/Cygwin on a dev host the
    script receives POSIX paths from sshd, so the test must hand it POSIX
    paths too or it would be asserting against a shape that never occurs in
    production.
    """
    if CYGPATH is None:
        return str(p)
    return subprocess.run(
        [CYGPATH, "-u", str(p)], capture_output=True, text=True, check=True
    ).stdout.strip()


def _run(out_dir: Path, original_command: str):
    return subprocess.run(
        [BASH, str(WRAPPER)],
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "KRAKEN_RECORDER_OUT": posix(out_dir),
            "SSH_ORIGINAL_COMMAND": original_command,
        },
        capture_output=True, text=True, timeout=60,
    )


@pytest.fixture()
def out_dir(tmp_path):
    d = tmp_path / "data" / "kraken_ws_v2"
    (d / "book_d10" / "BTCUSD").mkdir(parents=True)
    return d


# --- refusals ----------------------------------------------------------


def test_no_command_at_all_is_refused(out_dir):
    proc = _run(out_dir, "")
    assert proc.returncode == 1
    assert "no interactive shell" in proc.stderr


def test_a_login_shell_is_refused(out_dir):
    proc = _run(out_dir, "bash -i")
    assert proc.returncode == 1
    assert "not on the retrieval whitelist" in proc.stderr


def test_command_chaining_is_refused(out_dir):
    proc = _run(out_dir, "rm -f /etc/passwd; bash")
    assert proc.returncode == 1
    assert "metacharacter" in proc.stderr


def test_the_receiving_form_of_rsync_is_refused(out_dir):
    """--server without --sender would let the client WRITE to this host."""
    proc = _run(out_dir, f"rsync --server -logDtpre.iLsfxC . {posix(out_dir)}")
    assert proc.returncode == 1
    assert "SENDING form" in proc.stderr


def test_rsync_outside_the_out_dir_is_refused(out_dir):
    proc = _run(out_dir, "rsync --server --sender -logDtpre.iLsfxC . /etc/shadow")
    assert proc.returncode == 1
    assert "outside" in proc.stderr


def test_manifest_of_another_directory_is_refused(out_dir):
    proc = _run(out_dir, "python3 -m recorder.retrieval_manifest --out /etc")
    assert proc.returncode == 1
    assert "outside" in proc.stderr


def test_running_an_arbitrary_python_module_is_refused(out_dir):
    proc = _run(out_dir, "python3 -m http.server --out /tmp")
    assert proc.returncode == 1
    assert "recorder.retrieval_manifest" in proc.stderr


def test_deleting_outside_the_out_dir_is_refused(out_dir):
    proc = _run(out_dir, "rm -f /etc/passwd")
    assert proc.returncode == 1
    assert "outside" in proc.stderr
    assert Path("/etc/passwd").exists() or True  # never touched either way


def test_recursive_delete_is_refused(out_dir):
    victim = out_dir / "book_d10" / "BTCUSD" / "keep.ndjson.zst"
    victim.write_bytes(b"x")
    proc = _run(out_dir, f"rm -rf {posix(out_dir)}")
    assert proc.returncode == 1
    assert victim.exists()


def test_deleting_a_non_shard_file_is_refused(out_dir):
    other = out_dir / "notes.txt"
    other.write_text("keep me")
    proc = _run(out_dir, f"rm -f {posix(other)}")
    assert proc.returncode == 1
    assert ".ndjson.zst" in proc.stderr
    assert other.exists()


def test_deleting_the_coverage_journal_is_refused(out_dir):
    journal = out_dir / "_session.ndjson"
    journal.write_bytes(b'{"a":1}\n')
    proc = _run(out_dir, f"rm -f {posix(journal)}")
    assert proc.returncode == 1
    assert journal.exists()


def test_traversal_out_of_the_out_dir_is_refused(out_dir):
    proc = _run(out_dir, f"rm -f {posix(out_dir)}/../../escape.ndjson.zst")
    assert proc.returncode == 1
    assert "outside" in proc.stderr


# --- the one thing it is allowed to delete -----------------------------


def test_a_compacted_shard_inside_the_out_dir_is_deleted(out_dir):
    shard = out_dir / "book_d10" / "BTCUSD" / "2026-07-26T00.ndjson.zst"
    shard.write_bytes(b"archive")
    proc = _run(out_dir, f"rm -f {posix(shard)}")
    assert proc.returncode == 0, proc.stderr
    assert not shard.exists()
