"""
E-025 finale -- tests for the one-command killed-run gate (tools/killed_run_gate.py).

The gate's proofs drive the REAL run_tool_worker via plain module-attribute
assignment (rpr.ROOT / rpr.CAMPAIGN_STATE_PATH / rpr.subprocess.run), which leaks
process-wide. So this wrapper NEVER calls those proofs in-process -- it runs the tool
as a SUBPROCESS, exactly the way Jeremy runs it, and asserts on rc + captured output.
(The per-proof, isolated coverage lives in test_trial_accounting_characterization.py,
which uses the pure build_kill_summary builder under pytest monkeypatch.)

The cp1252 guard is the load-bearing one: it spawns the tool under
PYTHONIOENCODING=cp1252:strict -- the Windows-console encoder -- and goes RED if the
driver's contextlib.redirect_stdout wrapper around the emoji-printing pipeline is
removed (reproduced: '✅' -> UnicodeEncodeError). pytest replaces sys.stdout with
its own capture object, so only a real child process reproduces the console; an
in-process assertion cannot. Prior art: tests/test_setup_run_cp1252.py.
"""
import os
import subprocess
import sys
from pathlib import Path

GATE = Path(__file__).parent.parent / "tools" / "killed_run_gate.py"


def test_gate_all_proofs_pass_as_subprocess():
    proc = subprocess.run(
        [sys.executable, str(GATE)],
        capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, f"rc={proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    assert "VERDICT: ALL PROOFS PASS (8/8)" in proc.stdout
    # Every proof, not just the verdict tally.
    assert proc.stdout.count("[PASS]") == 8
    assert "[FAIL]" not in proc.stdout


def test_gate_is_cp1252_safe_windows_console_guard():
    """R-P9: the tool must run clean on a Windows cp1252 console. The pipeline prints
    emoji; the driver captures that stdout via redirect_stdout(io.StringIO()) so it
    never reaches the console encoder. Remove that wrapper and this goes RED
    (UnicodeEncodeError on '✅')."""
    env = {**os.environ, "PYTHONIOENCODING": "cp1252:strict"}
    proc = subprocess.run(
        [sys.executable, str(GATE)],
        capture_output=True, text=True, timeout=120, env=env,
    )
    assert proc.returncode == 0, f"rc={proc.returncode}\nstderr:\n{proc.stderr}"
    assert "UnicodeEncodeError" not in proc.stderr
    assert "VERDICT: ALL PROOFS PASS (8/8)" in proc.stdout
