"""CUL-12: setup_run.py's emoji status prints must not crash on a Windows
cp1252 console.

An unattended campaign run redirects/pipes stdout, so Windows drops from the
interactive console's UTF-8 to the locale codepage (cp1252 on a default install)
and print() raises UnicodeEncodeError on the first emoji byte it cannot encode.
PYTHONIOENCODING=cp1252:strict reproduces that exact console on this Mac in a
child process — no Windows machine needed.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

_SR = Path(__file__).parent.parent

# Reassign ROOT to a throwaway dir so the scaffolder writes nowhere real, then
# run the full setup_run() path, which drives the six emoji prints in setup_run.py
# (lines 80/90/97/105/112/114).
_DRIVER = textwrap.dedent(
    """
    import sys, tempfile
    from pathlib import Path
    sys.path.insert(0, "workflow")
    import setup_run
    setup_run.ROOT = Path(tempfile.mkdtemp())
    setup_run.setup_run("run_cp1252_probe")
    """
)


def test_setup_run_survives_a_cp1252_console(tmp_path):
    driver = tmp_path / "driver.py"
    driver.write_text(_DRIVER, encoding="utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "cp1252:strict"}
    proc = subprocess.run(
        [sys.executable, str(driver)],
        cwd=_SR,
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "UnicodeEncodeError" not in proc.stderr
