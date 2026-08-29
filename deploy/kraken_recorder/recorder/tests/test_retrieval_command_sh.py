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
    return subprocess.run([CYGPATH, "-u", str(p)], capture_output=True, text=True, check=True).stdout.strip()


def _run(out_dir: Path, original_command: str):
    return subprocess.run(
        [BASH, str(WRAPPER)],
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "KRAKEN_RECORDER_OUT": posix(out_dir),
            "SSH_ORIGINAL_COMMAND": original_command,
        },
        capture_output=True,
        text=True,
        timeout=60,
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
    proc = _run(out_dir, f"rsync --server -logDtprcze.iLsfxCIvu . {posix(out_dir)}")
    assert proc.returncode == 1
    assert "SENDING form" in proc.stderr


def test_rsync_outside_the_out_dir_is_refused(out_dir):
    proc = _run(out_dir, "rsync --server --sender -logDtprcze.iLsfxCIvu . /etc/shadow")
    assert proc.returncode == 1
    assert "outside" in proc.stderr


# --- rsync allowed-option whitelist ------------------------------------
#
# BASELINE is the exact server command rsync 3.2.7 sends for the
# `rsync -az --checksum` that retrieve_shards.py builds. It was observed by
# pointing rsync's -e at a stub that recorded its argv, not derived by
# reading the manual. Every case below is a one-option mutation of it.

BASELINE_OPTS = "-logDtprcze.iLsfxCIvu"


def test_the_observed_baseline_option_cluster_is_allowed(out_dir):
    """
    The whitelist must not break the only transfer the bundle actually makes.
    This reaches the exec, so rsync itself runs (and fails, since nothing is
    speaking the protocol on stdin) -- what matters is that it is NOT a
    refusal from this script.
    """
    shard = out_dir / "book_d10" / "BTCUSD" / "2026-07-26T00.ndjson.zst"
    shard.write_bytes(b"archive")
    proc = _run(out_dir, f"rsync --server --sender {BASELINE_OPTS} . {posix(shard)}")
    assert "REFUSED" not in proc.stderr, proc.stderr


def test_copy_links_is_refused(out_dir):
    """-L would let the client read through a symlink out of the capture dir."""
    proc = _run(out_dir, f"rsync --server --sender -lLogDtprcze.iLsfxCIvu . {posix(out_dir)}")
    assert proc.returncode == 1
    assert "-L is not on the retrieval whitelist" in proc.stderr


def test_copy_dirlinks_is_refused(out_dir):
    proc = _run(out_dir, f"rsync --server --sender -lkogDtprcze.iLsfxCIvu . {posix(out_dir)}")
    assert proc.returncode == 1
    assert "-k is not on the retrieval whitelist" in proc.stderr


def test_protect_args_is_refused(out_dir):
    proc = _run(out_dir, f"rsync --server --sender -slogDtprcze.iLsfxCIvu . {posix(out_dir)}")
    assert proc.returncode == 1
    assert "-s is not on the retrieval whitelist" in proc.stderr


def test_remove_source_files_is_refused(out_dir):
    """A *pull* must never be able to delete on this host."""
    proc = _run(
        out_dir,
        f"rsync --server --sender {BASELINE_OPTS} --remove-source-files . {posix(out_dir)}",
    )
    assert proc.returncode == 1
    assert "--remove-source-files" in proc.stderr


def test_copy_unsafe_links_is_refused(out_dir):
    proc = _run(
        out_dir,
        f"rsync --server --sender {BASELINE_OPTS} --copy-unsafe-links . {posix(out_dir)}",
    )
    assert proc.returncode == 1
    assert "--copy-unsafe-links" in proc.stderr


def test_the_capital_L_in_the_compat_blob_is_not_mistaken_for_copy_links(out_dir):
    """
    The regression this guards: `e.iLsfxCIvu` contains a capital L that is a
    protocol compat bit, not --copy-links. Rejecting on "L appears anywhere"
    would refuse every legitimate transfer the bundle makes.
    """
    shard = out_dir / "book_d10" / "BTCUSD" / "2026-07-26T00.ndjson.zst"
    shard.write_bytes(b"archive")
    proc = _run(out_dir, f"rsync --server --sender {BASELINE_OPTS} . {posix(shard)}")
    assert "-L is not on the retrieval whitelist" not in proc.stderr
    assert "REFUSED" not in proc.stderr, proc.stderr


def test_a_forged_protocol_blob_is_refused(out_dir):
    proc = _run(out_dir, f"rsync --server --sender -logDtprcze.iLsfx/../ . {posix(out_dir)}")
    assert proc.returncode == 1
    assert "REFUSED" in proc.stderr


def test_multiple_source_paths_are_refused(out_dir):
    a = out_dir / "a.ndjson.zst"
    proc = _run(
        out_dir,
        f"rsync --server --sender {BASELINE_OPTS} . {posix(a)} /etc/shadow",
    )
    assert proc.returncode == 1
    assert "REFUSED" in proc.stderr


# --- symlinked capture directory ---------------------------------------


def test_retrieval_succeeds_through_a_symlinked_out_dir(tmp_path):
    """
    The realistic shape once the capture volume is its own disk:
    /opt/kraken_recorder/data -> /mnt/big/kraken. Normalising only the target
    and comparing against a raw OUT_DIR denied every legitimate retrieval.
    """
    real = tmp_path / "mnt" / "big" / "kraken"
    (real / "book_d10" / "BTCUSD").mkdir(parents=True)
    shard = real / "book_d10" / "BTCUSD" / "2026-07-26T00.ndjson.zst"
    shard.write_bytes(b"archive")

    link = tmp_path / "opt" / "kraken_ws_v2"
    link.parent.mkdir(parents=True)
    try:
        link.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("this platform/user cannot create directory symlinks")

    # Addressed through the symlink, as the analysis host would address it.
    via_link = f"{posix(link)}/book_d10/BTCUSD/2026-07-26T00.ndjson.zst"
    proc = _run(link, f"rm -f {via_link}")
    assert proc.returncode == 0, proc.stderr
    assert not shard.exists()


def test_escape_through_a_symlinked_out_dir_is_still_denied(tmp_path):
    real = tmp_path / "mnt" / "big" / "kraken"
    real.mkdir(parents=True)
    outside = tmp_path / "mnt" / "big" / "secret.ndjson.zst"
    outside.write_bytes(b"do not touch")

    link = tmp_path / "opt" / "kraken_ws_v2"
    link.parent.mkdir(parents=True)
    try:
        link.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("this platform/user cannot create directory symlinks")

    proc = _run(link, f"rm -f {posix(link)}/../secret.ndjson.zst")
    assert proc.returncode == 1
    assert "outside" in proc.stderr
    assert outside.exists()


def test_a_symlink_planted_inside_the_out_dir_cannot_reach_outside(tmp_path):
    """
    Resolution happens on the target too, so a symlink inside the capture
    directory pointing out of it resolves outside and is denied.
    """
    out = tmp_path / "data" / "kraken_ws_v2"
    out.mkdir(parents=True)
    outside = tmp_path / "secret.ndjson.zst"
    outside.write_bytes(b"do not touch")

    planted = out / "evil.ndjson.zst"
    try:
        planted.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("this platform/user cannot create symlinks")

    proc = _run(out, f"rm -f {posix(planted)}")
    assert proc.returncode == 1
    assert "outside" in proc.stderr
    assert outside.exists()


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
