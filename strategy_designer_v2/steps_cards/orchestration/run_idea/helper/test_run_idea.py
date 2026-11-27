"""Tests of run_idea's own logic (no model call, no backtest): the lines it runs, its refusals, its row and table."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_idea as r  # noqa: E402


def test_the_lines_are_the_active_ones():
    ids = [lid for lid, _ in r.active_lines()]
    assert ids == ["7.a", "7.b", "7.c", "7.d", "7.e", "7.g"]   # 7.f was deleted (operator, 2026-11-21)


def test_an_idea_without_its_fields_is_refused():
    with pytest.raises(SystemExit):
        r.check_idea("---\nbrief: 002_x\n---\nIdea: something.\n")
    with pytest.raises(SystemExit):
        r.check_idea("---\ninstruments: BTC\n---\nIdea: a.\nConsequence: b.\n")
    assert r.check_idea("---\nbrief: 002_x\nbar: 1d\n---\nIdea: a.\nConsequence: b.\n")["bar"] == "1d"


def test_costs_are_read_from_the_helpers_output():
    out = "plan (adapted): x\ncost: 0.2974 USD, attempts: 1\n7.e N: 8 findings; cost 0.3528 USD\n"
    assert abs(sum(float(c) for c in r.COST.findall(out)) - 0.6502) < 1e-9


def test_index_lines_and_the_table(tmp_path):
    idx = tmp_path / "INDEX.md"
    idx.write_text("A_1d: not run: entry condition not met (step 5: confirmed; step 6: x)\nB_1d: 2 ideas (2 explorations)\n")
    assert r.index_says(idx, "A_1d").startswith("not run") and r.index_says(idx, "C_1d") is None
    r.write_row(tmp_path / "t", {"idea": "A", "parent": None, "step3": "plan", "step5": "inconclusive (+0.61)",
                                 "step6": "profitable enough", "step7": {"7.e": "A.e1_x"}, "cost": 1.5})
    r.write_row(tmp_path / "t", {"idea": "A", "parent": None, "step3": "plan", "step5": "confirmed (+2.20)",
                                 "step6": "profitable enough", "step7": {}, "cost": 0.3})
    rows = json.loads((tmp_path / "t" / "table.json").read_text())
    assert len(rows) == 1 and rows[0]["step5"].startswith("confirmed")   # one row per idea, the latest
    assert "| A | - | plan | confirmed (+2.20) |" in (tmp_path / "t" / "table.md").read_text()


def test_a_run_name_ends_in_run():
    sys.argv = ["run_idea.py", "x.md", "--run", "demo", "--python", "python3"]
    with pytest.raises(SystemExit):
        r.main()


def test_a_resumed_run_does_not_copy_a_file_onto_itself(tmp_path):
    f = tmp_path / "brief.md"
    f.write_text("x")
    r.copy_into(f, f)                       # no error
    r.copy_into(f, tmp_path / "copy.md")
    assert (tmp_path / "copy.md").read_text() == "x"


def test_the_journal_records_called_and_skipped_steps(tmp_path, monkeypatch):
    monkeypatch.setattr(r, "STEPS", tmp_path)
    monkeypatch.setattr(r, "call", lambda cmd: ("cost: 0.25 USD\n", 0.25, 0))
    out = tmp_path / "plan.md"
    out.write_text("p")
    j = r.Journal(tmp_path / "t", "demo_run", "X_1d")
    j.step("step3_plan", ["make_test_plan.py"], [out], done=False)
    j.step("step3_plan", ["make_test_plan.py"], [out], done=True)
    lines = [json.loads(l) for l in (tmp_path / "t" / "journal.jsonl").read_text().splitlines()]
    assert [l["action"] for l in lines] == ["called", "skipped: its output exists"]
    assert lines[0]["usd"] == 0.25 and lines[1]["usd"] == 0.0 and lines[0]["outputs"] == ["plan.md"]
    assert (tmp_path / "t" / "logs" / "X_1d" / "step3_plan.txt").read_text() == "cost: 0.25 USD\n"
    assert j.use["step3_plan"]["usd"] == 0.25


def test_model_calls_are_read_and_a_killed_call_is_marked(tmp_path, monkeypatch):
    out = ("model call: 41.2 s; tokens: input 10, cache read 0, cache write 900, output 2000 (thinking 1500); 0.3100 USD; "
           "stop: end_turn\nanswer refused: x\nmodel call: killed after 900 s; cost unknown\n"
           "7.b X: 3 findings; cost 0.3100 USD\n")
    calls = r.model_calls(out)
    assert calls == [{"seconds": 41.2, "usd": 0.31}, {"seconds": 900.0, "usd": None}]
    monkeypatch.setattr(r, "STEPS", tmp_path)
    monkeypatch.setattr(r, "call", lambda cmd: (out, 0.31, 0))
    j = r.Journal(tmp_path / "t", "demo_run", "X_1d")
    j.step("step7_7.b", ["analyse.py"], [], done=False)
    e = json.loads((tmp_path / "t" / "journal.jsonl").read_text())
    assert e["model_calls"] == 2 and e["longest_call_seconds"] == 900.0
    assert e["action"] == "called: 1 model call(s) killed after the timeout, cost unknown"


def test_a_verdict_without_a_main_measure_is_its_status():
    assert r.verdict_label({"status": "mismatch", "main_measure": None}) == "mismatch"
    assert r.verdict_label({"status": "confirmed", "main_measure": {"statistic": {"value": 2.931}}}) == "confirmed (+2.93)"
    assert r.verdict_label(None) == "no verdict"


def test_a_failed_step_stops_the_run_and_a_refused_call_says_so(tmp_path, monkeypatch):
    # night 3, 2026-11-21: step 3 called again failed on the usage limit, and its older refusal was read as its answer
    import pytest
    monkeypatch.setattr(r, "STEPS", tmp_path)
    j = r.Journal(tmp_path / "t", "demo_run", "X_1d")
    old = tmp_path / "plan.md"; old.write_text("an earlier answer")
    monkeypatch.setattr(r, "call", lambda cmd: ("model call refused by the service: limit\n", 0.0, r.SERVICE_REFUSED))
    with pytest.raises(SystemExit) as e:
        j.step("step3_plan", ["x"], [old], done=False, required=True)
    assert e.value.code == r.SERVICE_REFUSED                         # stopped, to be retried; the old plan not read
    with pytest.raises(SystemExit) as e:
        j.step("step7_7.d", ["x"], [old], done=False)                # any step: a refused call stops the run
    assert e.value.code == r.SERVICE_REFUSED
    monkeypatch.setattr(r, "call", lambda cmd: ("Traceback: a bug\n", 0.0, 1))
    with pytest.raises(SystemExit) as e:
        j.step("step3_plan", ["x"], [old], done=False, required=True)
    assert "its helper failed (exit 1)" in str(e.value.code)          # a required step that fails: the idea fails
    out, cost = j.step("step7_7.d", ["x"], [old], done=False)         # a line that fails: recorded, the run goes on
    assert cost == 0.0
    lines = (tmp_path / "t" / "journal.jsonl").read_text().splitlines()
    assert all("its helper failed" in l for l in lines)


def _fake_run(tmp_path, monkeypatch, data_use=None):
    """run_idea.main on one idea with every step replaced by a fake that writes its result file: the idea is confirmed
    and profitable enough. Returns the names of the helpers called."""
    tmp_path.mkdir(parents=True)
    monkeypatch.setattr(r, "STEPS", tmp_path)
    monkeypatch.setattr(r, "HERE", tmp_path / "orchestration" / "run_idea" / "helper")
    run, rid = "demo_run", "001-01_x_1d"
    if data_use is not None:
        (tmp_path / "orchestration" / "loop" / run).mkdir(parents=True)
        (tmp_path / "orchestration" / "loop" / run / "data_use.json").write_text(json.dumps(data_use))
    idea, brief = tmp_path / "001-01_x.md", tmp_path / "001_b.md"
    idea.write_text("---\nbrief: 001_b\n---\nIdea: a.\nConsequence: b.\n")
    brief.write_text("b")
    f = r.folders(run)
    called, calls = [], []

    def fake(cmd):
        name = Path(str(cmd[0])).name
        called.append(name)
        if name == "make_test_plan.py":
            f["plans"].mkdir(parents=True, exist_ok=True)
            (f["plans"] / f"{rid}.md").write_text("---\noutcome: plan\n---\n")
        elif name == "run_backtest.py":
            (f["backtests"] / rid).mkdir(parents=True, exist_ok=True)
            (f["backtests"] / rid / "run.md").write_text("x")
        elif name == "make_verdict.py":
            (f["verdicts"] / rid).mkdir(parents=True, exist_ok=True)
            (f["verdicts"] / rid / "result.json").write_text(json.dumps({"status": "confirmed", "main_measure": None}))
        elif name == "check_profitability.py":
            (f["checks"] / rid).mkdir(parents=True, exist_ok=True)
            (f["checks"] / rid / "result.json").write_text(json.dumps({"status": "profitable enough", "measures": []}))
        elif name == "common_record.py":
            b = tmp_path / "04_backtest" / run / "common" / "backtests" / rid
            b.mkdir(parents=True, exist_ok=True)
            (b / "chart_bars.csv.gz").write_text("")
            (tmp_path / "orchestration" / "common_record" / run).mkdir(parents=True, exist_ok=True)
            (tmp_path / "orchestration" / "common_record" / run / f"{rid}.json").write_text("{}")
        calls.append([str(c) for c in cmd])
        return "", 0.0, 0

    monkeypatch.setattr(r, "call", fake)
    monkeypatch.setattr(r.wishes, "unblocked", lambda plan: False)
    monkeypatch.setattr(sys, "argv", ["run_idea.py", str(idea), "--run", run, "--python", "py", "--brief", str(brief)])
    r.main()
    _fake_run.calls = calls
    return called


def test_the_common_record_only_in_the_data_use_mode(tmp_path, monkeypatch):
    """Step 9 (orchestration/common_record): called after step 6 for a candidate only when the loop's data_use.json
    says version 2; without the file (every run today) or with another version, nothing changes."""
    assert "common_record.py" not in _fake_run(tmp_path / "a", monkeypatch)
    assert "common_record.py" not in _fake_run(tmp_path / "b", monkeypatch, {"version": 1})
    called = _fake_run(tmp_path / "c", monkeypatch, {"version": 2})
    assert called.index("common_record.py") == called.index("chart_files.py") + 1     # right after step 6's files
    assert r.data_use_version("nothing_run") is None


def test_the_portfolio_update_is_called_only_in_data_use_version_2_with_a_common_record(tmp_path, monkeypatch):
    monkeypatch.setattr(r, "STEPS", tmp_path)
    assert r.data_use_version("a_run") is None                          # no data_use.json: today's runs
    (tmp_path / "orchestration/loop/a_run").mkdir(parents=True)
    (tmp_path / "orchestration/loop/a_run/data_use.json").write_text('{"version": 2}')
    assert r.data_use_version("a_run") == 2
    assert not r.has_common_record("a_run", "x_1d")
    (tmp_path / "04_backtest/a_run/common/backtests/x_1d").mkdir(parents=True)
    (tmp_path / "04_backtest/a_run/common/backtests/x_1d/chart_bars.csv.gz").write_text("")
    assert not r.has_common_record("a_run", "x_1d")                    # the result file too
    (tmp_path / "orchestration/common_record/a_run").mkdir(parents=True)
    (tmp_path / "orchestration/common_record/a_run/x_1d.json").write_text("{}")
    assert r.has_common_record("a_run", "x_1d")


def test_the_new_data_use_runs_its_steps_in_order(tmp_path, monkeypatch):
    """The three parts joined (common/data_use.md, 2026-11-27): in data use 2, step 4 reads the run's data_use.json,
    the common record follows step 6's files, the unseen test is not run (step 9 replaces it), and the portfolio
    update follows the common record. Without the file, the old order: no --data-use, the unseen test, no step 9 or 10."""
    old = _fake_run(tmp_path / "a", monkeypatch)
    old_calls = _fake_run.calls
    assert "unseen_test.py" in old and "common_record.py" not in old and "update.py" not in old
    assert not any("--data-use" in c for c in old_calls)
    new = _fake_run(tmp_path / "b", monkeypatch, {"version": 2})
    new_calls = _fake_run.calls
    step4 = next(c for c in new_calls if Path(c[0]).name == "run_backtest.py")
    assert step4[step4.index("--data-use") + 1].endswith("orchestration/loop/demo_run/data_use.json")
    assert "unseen_test.py" not in new
    assert new.index("chart_files.py") < new.index("common_record.py") < new.index("update.py")
