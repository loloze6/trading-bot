"""
supervise.sh: relaunches a crash, refuses to relaunch a guard abort.

Same stub-recorder contract regardless of host: exercises the restart loop
(arg parsing, exit-code branching, backoff arithmetic, restart-rate cap, and
journal_mark invocation) for real, under whatever bash is on this machine's
PATH. This proves the SCRIPT's own logic; it does not prove anything that
depends on being on an actual Linux kernel/filesystem (disk semantics,
systemd) if this happens to run on a non-Linux dev host — see README.md's
"what's tested vs. what to verify yourself" note.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from recorder.disk_guard import EXIT_DISK_GUARD_ABORT
from recorder.journal import JOURNAL_FILENAME, load_records

# supervise.sh lives at the bundle root, one level above the `recorder`
# package (recorder/tests/test_supervisor_sh.py -> recorder/ -> bundle root).
SUPERVISOR = Path(__file__).resolve().parents[2] / "supervise.sh"
BASH = shutil.which("bash")

pytestmark = pytest.mark.skipif(BASH is None, reason="no bash on this machine")


def _stub(tmp_path: Path, codes) -> Path:
    """A fake recorder driven by a scripted sequence of exit codes."""
    counter = tmp_path / "invocations.txt"
    script = tmp_path / "stub_recorder.py"
    script.write_text(
        textwrap.dedent(f"""
        import sys
        from pathlib import Path
        counter = Path(r"{counter}")
        n = int(counter.read_text()) if counter.exists() else 0
        n += 1
        counter.write_text(str(n))
        codes = {list(codes)!r}
        sys.exit(codes[min(n, len(codes)) - 1])
    """),
        encoding="utf-8",
    )
    return script


def _run(tmp_path, codes, extra=()):
    out = tmp_path / "out"
    out.mkdir()
    stub = _stub(tmp_path, codes)
    proc = subprocess.run(
        [
            BASH,
            str(SUPERVISOR),
            "--out",
            str(out),
            "--python-exe",
            sys.executable,
            "--recorder-command",
            str(stub),
            "--backoff-initial-seconds",
            "0",
            "--log-file",
            str(tmp_path / "recorder.log"),
            *extra,
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    invocations = tmp_path / "invocations.txt"
    return (
        proc,
        int(invocations.read_text()) if invocations.exists() else 0,
        load_records(out / JOURNAL_FILENAME),
        out,
    )


def test_a_crash_is_relaunched_and_the_gap_is_attested(tmp_path):
    proc, invocations, records, _out = _run(tmp_path, codes=[1, 0])

    assert invocations == 2, f"expected one relaunch\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode == 0  # the second run stopped cleanly

    boundaries = [r for r in records if r["type"] == "RESTART_BOUNDARY"]
    assert len(boundaries) == 1
    assert boundaries[0]["exit_code"] == 1
    assert boundaries[0]["attempt"] == 1
    assert boundaries[0]["written_by"] == "supervisor"
    assert "restart #1" in proc.stdout


def test_a_disk_guard_abort_is_never_relaunched(tmp_path):
    proc, invocations, records, _out = _run(tmp_path, codes=[EXIT_DISK_GUARD_ABORT, 0])

    assert invocations == 1, "restarting into a full disk is a loop, not a recovery"
    assert proc.returncode == EXIT_DISK_GUARD_ABORT
    assert [r for r in records if r["type"] == "RESTART_BOUNDARY"] == []
    assert "DISK_GUARD_ABORT" in proc.stdout
    assert "NOT relaunching" in proc.stdout


def test_a_clean_exit_is_not_relaunched(tmp_path):
    """Ctrl-C / SIGTERM-to-clean-stop means stop."""
    proc, invocations, _records, _out = _run(tmp_path, codes=[0, 0])
    assert invocations == 1
    assert proc.returncode == 0
    assert "clean stop" in proc.stdout


def test_repeated_crashes_hit_the_restart_cap_and_give_up(tmp_path):
    proc, invocations, records, _out = _run(tmp_path, codes=[1, 1, 1, 1, 1], extra=("--max-restarts", "2"))
    # 2 relaunches allowed -> 3 launches, then the cap refuses a 4th.
    assert invocations == 3
    assert proc.returncode == 4
    assert "GIVING UP" in proc.stdout
    assert len([r for r in records if r["type"] == "RESTART_BOUNDARY"]) == 2


def test_every_restart_is_logged_with_its_reason(tmp_path):
    proc, _n, _records, _out = _run(tmp_path, codes=[7, 0])
    log = (tmp_path / "recorder.log").read_text(encoding="utf-8", errors="replace")
    assert "SUPERVISOR" in log
    assert "exit 7" in log


def test_the_guard_exit_code_literal_matches_the_python_constant():
    """
    supervise.sh must decide without running Python, so it carries the code as
    a literal. This is the only thing keeping the two from drifting apart into
    a supervisor that cheerfully restarts into a full disk.
    """
    text = SUPERVISOR.read_text(encoding="utf-8")
    assert f"EXIT_DISK_GUARD_ABORT={EXIT_DISK_GUARD_ABORT}" in text


def test_healthy_run_resets_the_backoff_ladder(tmp_path):
    """
    A run that stays up >= --healthy-run-seconds resets backoff to the
    initial value rather than continuing to climb. Forced by setting
    --healthy-run-seconds to 0 so even the stub's near-instant exit counts
    as "healthy".
    """
    proc, invocations, _records, _out = _run(
        tmp_path,
        codes=[1, 1, 0],
        extra=("--healthy-run-seconds", "0", "--backoff-initial-seconds", "1"),
    )
    assert invocations == 3
    assert proc.returncode == 0
    assert "backoff ladder reset" in proc.stdout
