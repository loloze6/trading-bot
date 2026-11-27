"""Tests of common_record's own logic: the coins and windows, the final group never read, the files, the resume, the
shards. No backtest, no model call (the steps are replaced by fakes that write their result files)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common_record as C  # noqa: E402

WINDOWS = json.loads(C.WINDOWS.read_text())


def test_the_coins_are_the_portfolio_group_and_the_windows_the_research_file():
    assert len(C.coins.portfolio_group()) == 25 and len(WINDOWS) == 32
    assert not set(C.coins.portfolio_group()) & set(C.coins.FINAL)


def test_a_coin_window_only_after_the_coins_first_90_days_numbered_as_in_the_file(monkeypatch):
    import datetime as dt
    first = {"OLD": dt.date(2010, 1, 1), "NEW": dt.date(2019, 10, 3)}          # NEW's 91st day: 2020-01-01
    monkeypatch.setattr(C.coins, "dates", lambda c, data=None: [first[c] + dt.timedelta(days=i) for i in range(7000)])
    usable = lambda c, start: dt.date.fromisoformat(start) >= first[c] + dt.timedelta(days=90)
    per = C.coin_windows(WINDOWS, ["OLD", "NEW"], usable)
    assert per["OLD"] == (list(range(1, 33)), {})                              # w1..w32
    keep, left = per["NEW"]
    assert WINDOWS[keep[0] - 1]["test"]["start"] == "2020-01-01" and keep == list(range(13, 33))   # w13 is 2020-01 for both
    assert left == {"the coin's first 90 days": list(range(1, 13))}
    assert C.coin_windows(WINDOWS, ["X"], lambda c, s: False) == {"X": ([], {"the coin's first 90 days": list(range(1, 33))})}


def test_the_final_coins_are_never_read(monkeypatch):
    """data_use.md: the final group is used by no step until the final test. The 90-day rule reads each coin's first
    day: only portfolio coins are read, and the helper's code never names the final group."""
    read = []
    real = C.coins.first_day
    monkeypatch.setattr(C.coins, "first_day", lambda coin, data=C.coins.DATA: read.append(coin) or real(coin, data))
    C.coin_windows(WINDOWS, C.coins.portfolio_group())
    assert read and not set(read) & set(C.coins.FINAL)
    assert "FINAL" not in Path(C.__file__).read_text()
    assert not any(f"{c}USD" in Path(C.__file__).read_text() for c in C.coins.FINAL)


def test_the_shards_cover_every_book_once():
    books = list(range(120))
    parts = [C.shard(books, i, 6) for i in range(1, 7)]
    assert sorted(x for p in parts for x in p) == books and all(len(p) == 20 for p in parts)


def test_the_paying_books_come_from_the_register(tmp_path):
    reg = tmp_path / "books.json"
    reg.write_text(json.dumps([{"key": "b", "kind": "paying"}, {"key": "a", "kind": "confirmed"},
                               {"key": "a2", "kind": "paying"}]))
    assert [b["key"] for b in C.paying_books(reg)] == ["a2", "b"]


def test_files_index_and_resume(tmp_path, monkeypatch):
    steps, run, rid = tmp_path, "a_run", "001-01_x_1d"
    plan = steps / "03_test_plan" / run / "plans" / f"{rid}.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("---\ndata-bar: 1d\n---\n")
    (steps / "05_verification" / run / "verdicts" / rid).mkdir(parents=True)
    (steps / "05_verification" / run / "verdicts" / rid / "measure.py").write_text("def measure(bars): pass\n")
    calls = []

    def fake_backtest(plan, python, dest, windows, coin_list, usable):
        calls.append("step4")
        (dest / "BTCUSD" / "w1").mkdir(parents=True)
        (dest / "BTCUSD" / "w1" / "metrics.json").write_text("{}")
        (dest / "run.md").write_text("x")
        return f"{rid}: ran: BTCUSD 1/1 [1d, windows research_2016]"

    def fake(cmd):
        name = Path(str(cmd[0])).name
        calls.append(name)
        if name == "chart_files.py":
            (Path(str(cmd[1])) / "chart_bars.csv.gz").write_text("x")
        elif name == "make_verdict.py":
            d = Path(str(cmd[cmd.index("--verdicts-dir") + 1])) / rid
            d.mkdir(parents=True)
            (d / "result.json").write_text(json.dumps({"status": "rejected", "main_measure": {"value": -0.1}}))
        else:
            d = Path(str(cmd[cmd.index("--checks-dir") + 1])) / rid
            d.mkdir(parents=True)
            (d / "result.json").write_text(json.dumps({"status": "not profitable", "measures": [
                {"measure": "sharpe_min", "value": 0.3}, {"measure": "sharpe_vs_hold_min", "value": -0.2}]}))
        return 0

    monkeypatch.setattr(C, "backtest", fake_backtest)
    monkeypatch.setattr(C, "call", fake)
    monkeypatch.setattr(C, "commit", lambda: "abc")
    r = C.record_one(plan, run, "py", steps=steps, coin_list=["BTC", "ETH"])
    assert calls == ["step4", "chart_files.py", "make_verdict.py", "check_profitability.py"]
    assert (steps / "04_backtest" / run / "common" / "backtests" / rid / "chart_bars.csv.gz").exists()
    assert (steps / "05_verification" / run / "common" / "verdicts" / rid / "result.json").exists()
    assert (steps / "06_profitability" / run / "common" / "checks" / rid / "result.json").exists()
    res = json.loads((steps / "orchestration" / "common_record" / run / f"{rid}.json").read_text())
    for k in ("plan", "run", "coins_run", "windows_run", "made_utc", "commit"):
        assert k in res
    assert res["coins_asked"] == ["BTCUSD", "ETHUSD"] and res["coins_run"] == ["BTCUSD"] and res["windows_run"] == 1
    assert res["step6"]["status"] == "not profitable" and res["step6"]["measures"][0]["value"] == 0.3
    assert res["plan"] == f"03_test_plan/{run}/plans/{rid}.md" and r == res
    index = (steps / "orchestration" / "common_record" / "INDEX.md").read_text()
    assert f"{run}/{rid}: 1 of 2 coins, 1 coin-windows; step 5 rejected" in index
    made = res["made_utc"]
    C.record_one(plan, run, "py", steps=steps, coin_list=["BTC", "ETH"])         # a second call: no step called
    assert len(calls) == 4
    again = json.loads((steps / "orchestration" / "common_record" / run / f"{rid}.json").read_text())
    assert again["made_utc"] == made
    assert sum(1 for l in (steps / "orchestration" / "common_record" / "INDEX.md").read_text().splitlines()
               if l.startswith(f"{run}/{rid}:")) == 1


def test_step4_runs_each_coin_on_its_windows_with_the_files_numbering(tmp_path, monkeypatch):
    """One count before the engine runs (common/data_use.md, section 3): a coin's windows in its first 90 days, or
    before its history covers the plan's warm-up, are left out with their reason; the others keep the file's numbers."""
    import datetime as dt
    plan = tmp_path / "001-01_x_1d.md"
    plan.write_text("---\ndata-bar: 1d\n---\n")
    (tmp_path / "001-01_x_1d_config.json").write_text("{}")
    asked = {}
    monkeypatch.setattr(C.rb, "protocol", lambda py, sym, bar, folds, ws: {"windows": ws, "venue": {"label": "kraken"}})
    monkeypatch.setattr(C.coins, "plan_warmup", lambda py, cfg, bar: 400 * 86400)
    first = {"OLD": dt.date(2010, 1, 1), "NEW": dt.date(2023, 6, 1), "NONE": dt.date(2030, 1, 1)}
    monkeypatch.setattr(C.coins, "dates", lambda c, data=None: [first[c] + dt.timedelta(days=i) for i in range(7000)])

    def run_part(py, cfg, proto, numbers, cdir, pdir):        # step 4's own signature: the windows' numbers, a list
        asked[cdir.name] = (list(numbers), [w["label"] for w in proto["windows"]] == [WINDOWS[k - 1]["label"] for k in numbers],
                            pdir.name)
        return [(k, 1, 0.1, 2.0) for k in numbers], []

    monkeypatch.setattr(C.rb, "run_part", run_part)
    usable = lambda c, start: dt.date.fromisoformat(start) >= first[c] + dt.timedelta(days=90)
    line = C.backtest(plan, "py", tmp_path / "rec", WINDOWS, ["OLD", "NEW", "NONE"], usable)
    # NEW's first day 2023-06-01: its 91st day falls before w24 (2023-09), its 401st before w27 (2024-09)
    assert asked == {"OLDUSD": (list(range(1, 33)), True, "windows"), "NEWUSD": ([27, 28, 29, 30, 31, 32], True, "windows")}
    md = (tmp_path / "rec" / "run.md").read_text()
    assert ("- NEWUSD: 6 of 32 windows run. 26 left out by the data use (common/data_use.md, section 3): "
            + ", ".join(f"w{k}" for k in range(1, 24)) + " (the coin's first 90 days); w24, w25, w26 "
            "(the coin's history is shorter than the plan's warm-up: 400 days asked).") in md and "| w27 |" in md
    assert "- NONEUSD: 0 of 32 windows run. 32 left out by the data use" in md and "; 1d bars; windows research_2016" in md
    assert line.startswith("001-01_x_1d: ran: OLDUSD 32/32; NEWUSD 6/32 (26 left out by the data use); "
                           "NONEUSD not run (no window) (32 left out by the data use)")


def _book(steps, run, rid, config, plan=True, measure=True, record=True):
    if plan:
        (steps / "03_test_plan" / run / "plans").mkdir(parents=True, exist_ok=True)
        (steps / "03_test_plan" / run / "plans" / f"{rid}.md").write_text("---\n---\n")
        (steps / "03_test_plan" / run / "plans" / f"{rid}_config.json").write_text(json.dumps(config))
    if measure:
        (steps / "05_verification" / run / "verdicts" / rid).mkdir(parents=True, exist_ok=True)
        (steps / "05_verification" / run / "verdicts" / rid / "measure.py").write_text("def measure(bars): pass\n")
    if record:
        (steps / "04_backtest" / run / "backtests" / rid).mkdir(parents=True, exist_ok=True)
        (steps / "04_backtest" / run / "backtests" / rid / "config.json").write_text(json.dumps(config, indent=1))


def test_the_plan_is_found_in_its_own_run_first(tmp_path):
    rid = "001-01_x_1d"
    _book(tmp_path, "a_run", rid, {"k": 1})
    _book(tmp_path, "b_run", rid, {"k": 1})                         # the same config elsewhere: not looked at
    plan, measure, _ = C.find_plan("a_run", rid, tmp_path)
    assert plan.parts[-3] == "a_run" and measure.parts[-4] == "a_run"


def test_else_the_one_other_run_with_the_records_config(tmp_path):
    """paying_rerun_run (2026-11-27): steps 4 and 6 only; the plan is in the run whose plan's config is the record's."""
    rid = "001-01_x_1d"
    _book(tmp_path, "rerun_run", rid, {"k": 1}, plan=False)           # its own measure.py, no plan
    _book(tmp_path, "src_run", rid, {"k": 1})
    _book(tmp_path, "other_run", rid, {"k": 2})                      # another config: not this book's plan
    plan, measure, _ = C.find_plan("rerun_run", rid, tmp_path)
    assert plan.parts[-3] == "src_run" and measure.parts[-4] == "rerun_run"
    _book(tmp_path, "bare_run", rid, {"k": 1}, plan=False, measure=False)
    plan, measure, _ = C.find_plan("bare_run", rid, tmp_path)          # measure.py too from the matched run
    assert plan.parts[-3] == "src_run" and measure.parts[-4] == "src_run"


def test_no_match_or_several_matches_are_refused_naming_them(tmp_path):
    import pytest
    rid = "001-01_x_1d"
    _book(tmp_path, "rerun_run", rid, {"k": 1}, plan=False)
    with pytest.raises(C.Refused, match="0 other runs"):
        C.find_plan("rerun_run", rid, tmp_path)
    _book(tmp_path, "one_run", rid, {"k": 1})
    _book(tmp_path, "two_run", rid, {"k": 1})
    (tmp_path / "03_test_plan" / "two_run" / "plans" / f"{rid}.md").write_text("---\nfit: other\n---\n")
    with pytest.raises(C.Refused, match=r"2 other runs with its config whose plan or measure.py differ \(one_run, two_run\)"):
        C.find_plan("rerun_run", rid, tmp_path)
    _book(tmp_path, "norec_run", rid, {"k": 1}, plan=False, record=False)
    with pytest.raises(C.Refused, match="no record config"):
        C.find_plan("norec_run", rid, tmp_path)


def test_several_byte_identical_matches_are_one_plan(tmp_path):
    """designer, 2026-11-27: 010-03.e1 of paying_rerun_run, its plan in hold2_rerun_run and hold_paying_run, the
    same files: one plan, the first in sorted order, every match recorded."""
    import pytest
    rid = "001-01_x_1d"
    _book(tmp_path, "rerun_run", rid, {"k": 1}, plan=False, measure=False)
    _book(tmp_path, "b_run", rid, {"k": 1})
    _book(tmp_path, "a_run", rid, {"k": 1})
    plan, measure, matched = C.find_plan("rerun_run", rid, tmp_path)
    assert plan.parts[-3] == "a_run" and measure.parts[-4] == "a_run" and matched == ["a_run", "b_run"]
    (tmp_path / "05_verification" / "b_run" / "verdicts" / rid / "measure.py").write_text("def measure(bars): return 1\n")
    with pytest.raises(C.Refused, match="differ"):                 # the measure.py differ: refused
        C.find_plan("rerun_run", rid, tmp_path)
