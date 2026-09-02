"""CUL-213: run_phase1_research.py's emoji status prints must not crash on a
Windows cp1252 console.

The Phase-1 orchestrator prints emoji status lines on ~130 paths. An unattended
campaign redirects/pipes stdout, so Windows drops from the interactive console's
UTF-8 to the locale codepage (cp1252 on a default install) and print() raises
UnicodeEncodeError on the first emoji byte it cannot encode. This is the same
class already fixed for setup_run.py (CUL-12) and the PR#2 seal test (CUL-76).
PYTHONIOENCODING=cp1252:strict reproduces that exact console on this Mac in a
child process — no Windows machine needed. An in-process assertion cannot
reproduce it because pytest replaces sys.stdout with a capture buffer.
"""

import ast
import os
import subprocess
import sys
import textwrap
from pathlib import Path

_SR = Path(__file__).parent.parent
_MODULE = _SR / "workflow" / "run_phase1_research.py"

# Drive a real emoji-printing path in run_phase1_research: the refine-branch of
# determine_post_validation_route hits `print("🛑 Refinement limit reached ...")`
# (run_phase1_research.py:2367) with no file writes, so it exercises the module's
# stdout guard deterministically from trivial fixtures.
_DRIVER = textwrap.dedent(
    """
    import sys, tempfile
    from pathlib import Path
    import yaml
    sys.path.insert(0, "workflow")
    import run_phase1_research as r
    d = Path(tempfile.mkdtemp())
    (d / "artifacts").mkdir()
    (d / "artifacts" / "validation_decision.yaml").write_text(
        "status: refine\\n", encoding="utf-8"
    )
    (d / "pipeline_state.yaml").write_text(
        yaml.safe_dump(
            {
                "counters": {"refinements_used": 5},
                "governance": {"max_refinements_after_validation": 2},
            }
        ),
        encoding="utf-8",
    )
    route = r.determine_post_validation_route(d)
    assert route == "completed_rejected", route
    """
)


def test_run_phase1_research_survives_a_cp1252_console(tmp_path):
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


def test_driven_print_still_carries_a_non_ascii_glyph():
    """Guard against a vacuous pass: the subprocess test only proves cp1252
    safety while the driven path actually prints a non-ASCII glyph. If the
    "Refinement limit reached" print is ever de-emojified, the subprocess test
    would pass for the wrong reason — this makes that a loud failure instead."""
    src = _MODULE.read_text(encoding="utf-8")
    tree = ast.parse(src)
    driven = [
        seg
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
        and (seg := ast.get_source_segment(src, node))
        and "Refinement limit reached" in seg
    ]
    assert driven, "driven print 'Refinement limit reached' not found in module"
    assert any(ord(c) > 127 for c in driven[0]), (
        "the print the cp1252 subprocess test drives no longer contains a "
        "non-ASCII glyph — the subprocess test would pass vacuously"
    )
