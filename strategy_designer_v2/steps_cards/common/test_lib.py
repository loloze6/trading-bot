"""Tests of the shared helpers (common/lib.py): the header readers, the idea fields step 3 reads, atomic writes."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import child_id, common_text, first_child_number, header, header_fields, idea_code, idea_fields, write_atomic  # noqa: E402

STEP7_IDEA = """---
brief: 002_some-brief
source-idea: 002-03_some-idea
line: 7.d not profitable
backtest: 002-03_some-idea_1d
instruments: BTC, ETH
bar: 1d
period: folds A, D
---
Idea: While a coin's close is above its N-day average, the further above, the larger its rise over the next N days.
Consequence: Take longs further above the average.
Why:
- F1: a number measured on the data, t 3.1.
"""


def test_header_and_fields():
    lines, body = header(STEP7_IDEA)
    assert lines[0] == "brief: 002_some-brief" and body.startswith("Idea:")
    assert header_fields(STEP7_IDEA)["period"] == "folds A, D"
    assert header_fields("no header") == {}
    with pytest.raises(SystemExit):
        header("no header")


def test_idea_fields_keep_only_what_step3_reads():
    out = idea_fields(STEP7_IDEA)
    assert "Why" not in out and "t 3.1" not in out and "source-idea" not in out and "backtest" not in out
    assert out.splitlines() == ["---", "brief: 002_some-brief", "instruments: BTC, ETH", "bar: 1d",
                                "period: folds A, D", "---",
                                "Idea: While a coin's close is above its N-day average, the further above, the larger its rise over the next N days.",
                                "Consequence: Take longs further above the average."]
    with pytest.raises(SystemExit):
        idea_fields("---\nbrief: x\n---\nIdea: no consequence line\n")


def test_write_atomic_and_common_text(tmp_path):
    p = tmp_path / "f.md"
    write_atomic(p, "one")
    write_atomic(p, "two")
    assert p.read_text() == "two" and not (tmp_path / "f.md.tmp").exists()
    assert "Every idea" in common_text("idea_definition")


def test_the_line_a_model_call_prints():
    import lib
    d = {"usage": {"input_tokens": 5, "cache_read_input_tokens": 600, "cache_creation_input_tokens": 4000,
                   "output_tokens": 9000, "output_tokens_details": {"thinking_tokens": 7000}},
         "total_cost_usd": 0.41234, "stop_reason": "end_turn"}
    line = lib.call_line(d, 63.04)
    assert line == ("model call: 63.0 s; tokens: input 5, cache read 600, cache write 4000, output 9000 (thinking 7000); "
                    "0.4123 USD; stop: end_turn")
    assert "cost" not in line.split(";")[2]          # run_idea's "cost: X USD" pattern must not count it twice


def test_utc_now_is_a_full_utc_timestamp():
    import re
    from lib import utc_now
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", utc_now())


def test_a_call_the_service_refused_exits_with_its_own_code(monkeypatch):
    import json as _json, subprocess as _sp, pytest
    import lib as _lib
    class P:
        def __init__(self, out): self.stdout, self.stderr, self.returncode = out, "", 1
    for out, code in [(_json.dumps({"is_error": True, "result": "You've hit your limit", "total_cost_usd": 0}), _lib.SERVICE_REFUSED),
                      ("not json", _lib.SERVICE_REFUSED)]:
        monkeypatch.setattr(_sp, "run", lambda *a, _o=out, **k: P(_o))
        with pytest.raises(SystemExit) as e:
            _lib.call("m", "s", "r")
        assert e.value.code == code
    monkeypatch.setattr(_sp, "run", lambda *a, **k: P(_json.dumps({"is_error": True, "result": "bad answer", "total_cost_usd": 0.2})))
    with pytest.raises(SystemExit) as e:
        _lib.call("m", "s", "r")
    assert str(e.value.code).startswith("model call failed")          # a call that ran and failed: as before


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="end_with_parent acts on Linux only (prctl); elsewhere it does nothing, as its card says")
def test_a_helper_started_by_a_helper_ends_with_it(tmp_path):
    """Night 5: an orphan step 4 kept writing after its run was stopped. A child that imports lib, started by a parent
    that imports lib, ends when the parent is killed (SIGKILL: no clean-up of its own); a helper started from a shell
    is not marked, so it is never stopped this way."""
    import os, signal, subprocess, sys, time
    common = str(Path(__file__).resolve().parent)
    child = f"import sys; sys.path.insert(0, {common!r}); import lib, time; time.sleep(60)"
    parent = (f"import sys, subprocess; sys.path.insert(0, {common!r}); import lib; "
              f"p = subprocess.Popen([sys.executable, '-c', {child!r}]); print(p.pid, flush=True); p.wait()")
    env = {k: v for k, v in os.environ.items() if k != "CARDS_PARENT_PID"}      # as from a shell
    par = subprocess.Popen([sys.executable, "-c", parent], stdout=subprocess.PIPE, text=True, env=env)
    kid = int(par.stdout.readline())
    time.sleep(1)                                   # the child has imported lib
    assert par.poll() is None                       # the parent, started from a shell, is not stopped
    os.kill(par.pid, signal.SIGKILL); par.wait()
    for _ in range(50):
        try:
            os.kill(kid, 0)
        except ProcessLookupError:
            return                                  # the child ended
        if open(f"/proc/{kid}/stat").read().split()[2] == "Z":
            return                                  # ended, waiting to be reaped by init
        time.sleep(0.1)
    os.kill(kid, signal.SIGKILL)
    raise AssertionError("the child outlived its parent")


def test_an_idea_id_carries_its_lineage_code_and_its_own_name_only():
    """Topic 46 (operator, 2026-11-23): a child's id is its parent's lineage code, the line's letter and number, and its
    own short name; an id written before reads the same lineage code."""
    old = "022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_strong-nearness-power-reversals"
    assert idea_code(old) == "022-04.b1.d2"
    assert idea_code("022-04.b1.d2_strong-nearness-power-reversals") == "022-04.b1.d2"
    assert idea_code("022-04_signal-weights-carry-forward") == "022-04"
    assert idea_code(old + "_1d") == "022-04.b1.d2"                              # a record id: the bar is not a step
    assert child_id(old, "d", 1, "nearness-reversal-long") == "022-04.b1.d2.d1_nearness-reversal-long"
    deep = "022-04"
    for k in range(12):                                                         # twelve generations
        deep = child_id(deep, "d", 3, "a-short-name-of-about-forty-characters-x")
    assert len(f"{deep}_4h_config.json".encode()) < 120 and idea_code(deep).count(".") == 12


def test_a_lines_numbering_goes_on_across_the_runs_analyses_of_the_same_parent():
    """An idea tested on two bar sizes is analysed twice by the same line in a run: the second analysis numbers after the
    first, so a lineage code names one idea (retest_1h_run had 5 codes shared by two ideas)."""
    parent = "001-01_x.a1_y"
    assert first_child_number(parent, "c", []) == 1
    others = ["001-01_x.a1_y.c1_one", "001-01_x.a1_y.c2_two", "001-01.a1.c3_three", "001-01_x.a1_y.d1_other-line",
              "001-01_x.a2_z.c5_other-parent"]
    assert first_child_number(parent, "c", others) == 4
    assert first_child_number(parent, "d", others) == 2
