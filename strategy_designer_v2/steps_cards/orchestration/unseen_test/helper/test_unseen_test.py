"""Tests of unseen_test's own logic: the holds rule, the periods, the files and the resume. No backtest, no model call
(the steps' helpers are replaced by a fake that writes their result files)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import unseen_test as U  # noqa: E402

IN_SAMPLE = {"status": "confirmed", "main_measure": {"value": 0.02, "statistic": {"name": "t", "value": 3.1}}}


def check(sharpe, vs_hold):
    return {"status": "profitable enough", "measures": [{"measure": "sharpe_min", "value": sharpe},
                                                        {"measure": "sharpe_vs_hold_min", "value": vs_hold}]}


def verdict(value, t, status="inconclusive"):
    return {"status": status, "main_measure": {"value": value, "statistic": {"value": t}}}


def test_holds_needs_the_in_sample_sign_and_a_positive_sharpe():
    r = U.reading(IN_SAMPLE, verdict(0.01, 0.9), check(0.8, 0.7))
    assert r["holds"] and r["statistic"] == 0.9 and abs(r["holding_sharpe"] - 0.1) < 1e-12
    assert not U.reading(IN_SAMPLE, verdict(-0.01, -1.9), check(0.8, 0.7))["holds"]    # the measure turned
    assert not U.reading(IN_SAMPLE, verdict(0.01, 0.9), check(-0.2, 0.1))["holds"]     # the book lost
    assert U.reading(IN_SAMPLE, None, None)["holds"] is None                           # no data: not judged
    negative = {"main_measure": {"value": -0.03}}                                      # an idea measured below 0
    assert U.reading(negative, verdict(-0.01, -0.5), check(0.3, 0.1))["holds"]
    assert not U.reading(negative, verdict(0.0, 0.0), check(0.3, 0.1))["holds"]        # 0 has no sign


def test_the_periods_are_the_windows_files():
    assert U.periods() == sorted(p.stem for p in U.WINDOWS.glob("unseen_*.json"))
    assert "unseen_2026" in U.periods()


def test_files_in_the_run_and_resume(tmp_path, monkeypatch):
    steps = tmp_path
    rid, run = "001-01_x_1d", "a_run"
    (steps / "05_verification" / run / "verdicts" / rid).mkdir(parents=True)
    (steps / "05_verification" / run / "verdicts" / rid / "result.json").write_text(json.dumps(IN_SAMPLE))
    (steps / "05_verification" / run / "verdicts" / rid / "measure.py").write_text("def measure(bars): pass\n")
    plan = steps / "03_test_plan" / run / "plans" / f"{rid}.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("---\n---\n")
    (steps / "w").mkdir()
    for p in ("unseen_a", "unseen_b"):
        (steps / "w" / f"{p}.json").write_text("[]")
    calls = []

    def fake(cmd, period):
        calls.append(Path(str(cmd[0])).name)
        name = Path(str(cmd[0])).name
        if name == "run_backtest.py":
            root = Path(str(cmd[cmd.index("--out-root") + 1]))
            (root / rid / "BTCUSD" / "w1").mkdir(parents=True)
            (root / rid / "run.md").write_text("x")
            (root / rid / "BTCUSD" / "w1" / "metrics.json").write_text("{}")
        elif name == "chart_files.py":
            (Path(str(cmd[1])) / "chart_bars.csv.gz").write_text("x")
        elif name == "make_verdict.py":
            d = Path(str(cmd[cmd.index("--verdicts-dir") + 1])) / rid
            d.mkdir(parents=True)
            (d / "result.json").write_text(json.dumps(verdict(0.01, 1.2)))
        else:
            d = Path(str(cmd[cmd.index("--checks-dir") + 1])) / rid
            d.mkdir(parents=True)
            (d / "result.json").write_text(json.dumps(check(1.1, 1.0)))
        return 0

    monkeypatch.setattr(U, "STEPS", steps)
    monkeypatch.setattr(U, "WINDOWS", steps / "w")
    monkeypatch.setattr(U, "HERE", steps / "orchestration" / "unseen_test" / "helper")
    monkeypatch.setattr(U, "call", fake)
    monkeypatch.setattr(sys, "argv", ["unseen_test.py", str(plan), "--run", run, "--python", "py"])
    U.main()
    assert calls == ["run_backtest.py", "chart_files.py", "make_verdict.py", "check_profitability.py"] * 2
    assert (steps / "04_backtest" / run / "unseen_b" / "backtests" / rid / "run.md").exists()
    res = json.loads((steps / "orchestration" / "unseen_test" / run / f"{rid}.json").read_text())
    assert res["periods"]["unseen_a"]["holds"] and res["in_sample"]["statistic"] == 3.1
    assert (steps / "orchestration" / "unseen_test" / run / "INDEX.md").read_text() == \
        f"{rid}: unseen_a: holds; unseen_b: holds\n"
    calls.clear()
    U.main()                                         # a second call: every output exists, no step is called
    assert calls == []


def test_a_record_where_no_window_ran_is_run_again(tmp_path):
    rec = tmp_path / "rec"
    (rec / "BTCUSD").mkdir(parents=True)
    (rec / "run.md").write_text("- w1 not run: the dates were not fetched")
    assert not U.backtest_ran(rec)
    (rec / "BTCUSD" / "w1").mkdir()
    (rec / "BTCUSD" / "w1" / "metrics.json").write_text("{}")
    assert U.backtest_ran(rec)
    assert not U.backtest_ran(tmp_path / "none")
