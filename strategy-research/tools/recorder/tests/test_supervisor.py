"""
supervise.ps1: relaunches a crash, refuses to relaunch a guard abort.

Driven against a stub "recorder" that exits with a chosen code, so both paths
are exercised for real — same script, same exit-code handling, same journal
write — without a websocket, a disk, or a wait.

The distinction under test is the expensive one. Book-stream gaps are
permanently unrecoverable, so failing to relaunch after a crash silently
shortens the capture; relaunching after a DISK_GUARD_ABORT loops into a full
disk. Nothing else in the deploy tells these two exits apart.
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

SUPERVISOR = Path(__file__).resolve().parents[1] / "supervise.ps1"
POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")

pytestmark = pytest.mark.skipif(POWERSHELL is None, reason="no PowerShell host on this machine")


def _stub(tmp_path: Path, codes) -> Path:
    """
    A fake recorder that exits with `codes[n]` on its n'th invocation, counting
    invocations in a file so the supervisor's relaunch behaviour is observable.
    Unknown flags are ignored — the supervisor passes the real recorder's.
    """
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
            POWERSHELL,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(SUPERVISOR),
            "-Out",
            str(out),
            "-PythonExe",
            sys.executable,
            "-RecorderCommand",
            str(stub),
            "-BackoffInitialSeconds",
            "0",
            "-LogFile",
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
    """Ctrl-C means stop. The previous supervisor restarted through it."""
    proc, invocations, _records, _out = _run(tmp_path, codes=[0, 0])
    assert invocations == 1
    assert proc.returncode == 0
    assert "clean stop" in proc.stdout


def test_repeated_crashes_hit_the_restart_cap_and_give_up(tmp_path):
    proc, invocations, records, _out = _run(tmp_path, codes=[1, 1, 1, 1, 1], extra=("-MaxRestarts", "2"))
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


def test_the_supervisor_stays_pure_ascii():
    """
    PowerShell 5.1 reads a BOM-less `.ps1` as ANSI, not UTF-8. A typographic
    em-dash in a comment or a log message therefore arrives as U+201D -- which
    PowerShell accepts AS A STRING DELIMITER -- and the whole script becomes a
    parse error at a line nowhere near the dash. Found the hard way while
    writing this file. ASCII-only is the fix that does not depend on anyone
    remembering to save with a BOM.
    """
    text = SUPERVISOR.read_bytes()
    offending = [b for b in text if b > 0x7F]
    assert not offending, f"{len(offending)} non-ASCII byte(s) in supervise.ps1"


def test_the_guard_exit_code_literal_matches_the_python_constant():
    """
    supervise.ps1 must decide without running Python, so it carries the code as
    a literal. This is the only thing keeping the two from drifting apart into
    a supervisor that cheerfully restarts into a full disk.
    """
    text = SUPERVISOR.read_text(encoding="utf-8")
    assert f"$EXIT_DISK_GUARD_ABORT = {EXIT_DISK_GUARD_ABORT}" in text
