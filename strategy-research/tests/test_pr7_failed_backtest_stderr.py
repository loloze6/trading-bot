"""
PR-7 (run_098 defect: stderr lost on a failed backtest) -- protocol_execution
captured the child's stdout only, so a variant whose run_protocol.py exited 1
left no traceback (run_098 asset_ada). On the failed-backtest branch ONLY, the
child's full stderr is now saved to artifacts/variants/<variant>/
run_protocol_stderr.txt and its tail printed under the failure line. The recorded
failure reason ("run_protocol.py non-zero exit (N)") is unchanged; the success
path and the no-data-touched refusal path write and print nothing new.

The failing child here is a REAL process (sys.executable on a script that writes
to stderr and exits 1), run through the real subprocess.run.
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import protocol_refusal  # noqa: E402

from test_grid_evaluation import _windows_for_reducer  # noqa: E402
from test_e033_slice4a_variant_loop import _summary_for  # noqa: E402
from test_e061_c2_s2a_crashed_variant import (  # noqa: E402
    _setup_run, _grid_of, CRASH)

_REAL_RUN = subprocess.run
STDERR_FILE = rpr.FAILED_STDERR_FILENAME
N_LINES = 30  # more than the 20-line tail
STDERR_TEXT = "".join(f"stderrline {i:02d}\n" for i in range(1, N_LINES)) + \
    "Traceback-ish: ValueError: pr7-unique-marker\n"

_CHILD = (
    "import sys\n"
    "sys.stdout.write('child stdout line\\n')\n"
    "sys.stderr.write(open(sys.argv[1], encoding='utf-8', newline='').read())\n"
    "sys.exit(1)\n"
)


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _attempt(monkeypatch, tmp_path, run_id, *, fail=(), refuse=(), ok_stderr=""):
    """One protocol_execution attempt. Variants in `fail` run a real child
    process that writes STDERR_TEXT to stderr and exits 1; those in `refuse`
    exit EXIT_NO_DATA_TOUCHED with the token; the rest succeed (optionally
    writing `ok_stderr`)."""
    script = tmp_path / "failing_child.py"
    script.write_text(_CHILD, encoding="utf-8")
    text_file = tmp_path / "child_stderr_text.txt"
    text_file.write_text(STDERR_TEXT, encoding="utf-8", newline="")

    def _run(cmd, *a, **k):
        vid = Path(cmd[2]).parent.name
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        if vid in fail:
            return _REAL_RUN([sys.executable, str(script), str(text_file)], *a, **k)

        class _R:
            returncode, stdout, stderr = 0, "", ok_stderr
        if vid in refuse:
            _R.returncode = protocol_refusal.EXIT_NO_DATA_TOUCHED
            _R.stderr = f"{protocol_refusal.NO_DATA_TOUCHED_TOKEN}: x -- refusing.\n"
            return _R()
        summary = _summary_for(vid)
        summary["results"] = _windows_for_reducer([1.0, 2.0, 3.0])
        for r in summary["results"]:
            r["core"]["sharpe"] = 1.0
        (out / "protocol_summary.json").write_text(json.dumps(summary), encoding="utf-8")
        return _R()
    monkeypatch.setattr(rpr.subprocess, "run", _run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))


def _stderr_path(run_dir, vid):
    return run_dir / "artifacts" / "variants" / vid / STDERR_FILE


def test_failed_child_stderr_is_saved_and_its_tail_printed_with_the_failure_line(
        monkeypatch, tmp_path, capsys):
    run_dir = _setup_run("run_971")
    _attempt(monkeypatch, tmp_path, "run_971", fail={"design_v2"})
    out = capsys.readouterr().out

    saved = _stderr_path(run_dir, "design_v2")
    assert saved.read_bytes() == STDERR_TEXT.encode("utf-8")  # full text, byte for byte

    failure = "variant 'design_v2' failed (run_protocol.py exit 1)"
    assert failure in out
    after = out.split(failure, 1)[1]
    assert "last 20 of 30 lines" in after
    assert "pr7-unique-marker" in after            # the final line is in the tail
    assert "stderrline 29" in after and "stderrline 11" in after
    assert "stderrline 10" not in after            # only the last 20 lines
    assert "stderrline 01" not in out

    # the recorded failure reason is unchanged, and the other variants wrote nothing
    assert _grid_of(run_dir)["failed_variants"] == {"design_v2": CRASH}
    assert not _stderr_path(run_dir, "base").exists()
    assert not _stderr_path(run_dir, "asset_v2").exists()


def test_success_path_writes_no_file_and_prints_no_stderr(monkeypatch, tmp_path, capsys):
    run_dir = _setup_run("run_972")
    _attempt(monkeypatch, tmp_path, "run_972", ok_stderr="harmless warning on success\n")
    out = capsys.readouterr().out
    for vid in ("asset_v2", "base", "design_v2"):
        assert not _stderr_path(run_dir, vid).exists()
    assert "harmless warning on success" not in out
    assert "child stderr" not in out and "stderr saved" not in out
    assert "failed (run_protocol.py" not in out
    assert "failed_variants" not in _grid_of(run_dir)


def test_no_data_touched_refusal_path_is_unchanged(monkeypatch, tmp_path, capsys):
    run_dir = _setup_run("run_973")
    _attempt(monkeypatch, tmp_path, "run_973", refuse={"asset_v2"})
    out = capsys.readouterr().out
    assert not _stderr_path(run_dir, "asset_v2").exists()
    assert "child stderr" not in out
    assert "refused before any backtest" in out


def test_helper_short_empty_and_none_stderr(tmp_path, capsys):
    rpr._save_and_print_failed_stderr(tmp_path, "a\nb\n")
    out = capsys.readouterr().out
    assert "last 2 of 2 lines" in out and out.rstrip().endswith("a\nb")
    assert (tmp_path / STDERR_FILE).read_text(encoding="utf-8") == "a\nb\n"

    rpr._save_and_print_failed_stderr(tmp_path, "")
    assert "child stderr was empty" in capsys.readouterr().out
    assert (tmp_path / STDERR_FILE).read_bytes() == b""

    rpr._save_and_print_failed_stderr(tmp_path, None)
    assert "child stderr was empty" in capsys.readouterr().out


def test_helper_write_failure_does_not_raise(tmp_path, capsys):
    rpr._save_and_print_failed_stderr(tmp_path / "missing_dir", "x\n")
    out = capsys.readouterr().out
    assert "could not be saved" in out and "x" in out
