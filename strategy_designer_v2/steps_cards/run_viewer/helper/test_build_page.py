"""Run viewer: every figure on the page is a field of a file, or a count, sum, mean, product or largest of them."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_page as bp  # noqa: E402

ROOT = "001-01_rise-continues"
CHILD = ROOT + ".b1_rise-continues-more-coins"
WAITING = ROOT + ".g1_fall-rebounds"


def w(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text if isinstance(text, str) else json.dumps(text), encoding="utf-8")


def window(cards, bid, coin, k, ret, end):
    d = cards / f"04_backtest/x_run/backtests/{bid}/{coin}/w{k}"
    w(d / "metrics.json", {"core": {"net_return_pct": ret, "trade_count": k, "win_rate": 50.0},
                           "bar_equity": {"max_drawdown_pct": -2.0, "sharpe": 1.0, "exposure_pct": 30.0}})
    w(d / "manifest.json", {"data": {"end": end}, "created_utc": f"2026-11-17T0{k}:00:00+00:00"})


@pytest.fixture
def cards(tmp_path):
    c = tmp_path
    w(c / "runs" / "X_RUN.md", "# Run brief: x_run\n\n**Purpose.** See whether rises continue.\n\n**Scope.** one coin.\n")
    w(c / "01_brief/x_run/briefs/001_rises-continue.md", "---\n---\nRises continue.\n")
    w(c / "01_brief/x_run/briefs/INDEX.md", "001: rises continue\n")
    w(c / f"02_ideation/x_run/ideas/{ROOT}.md", "---\nbrief: 001\n---\nIdea: A rise continues.\nConsequence: lean long.\n")
    w(c / f"03_test_plan/x_run/plans/{ROOT}_1d.md",
      f"---\nidea: {ROOT}\noutcome: plan\nfit: exact\ndata-bar: 1d\n---\nFidelity:\n- kept\n")
    w(c / f"03_test_plan/x_run/plans/{CHILD}_1d.md",
      f"---\nidea: {CHILD}\noutcome: missing-components\n---\nFidelity:\n- x\nReason: No component reads volume.\nIt stops here.\n")
    w(c / "03_test_plan/x_run/plans/INDEX.md", "not a plan\n")
    w(c / f"02_ideation/x_run/ideas/{WAITING}.md", "---\nbrief: 001\nbar: 4h\n---\nIdea: A fall rebounds.\n")
    # two windows, given out of time order on purpose: w1 ends after w2
    window(c, f"{ROOT}_1d", "BTCUSD", 1, 10.0, "2021-04-30 00:00:00")
    window(c, f"{ROOT}_1d", "ETHUSD", 1, 20.0, "2021-04-30 00:00:00")
    window(c, f"{ROOT}_1d", "BTCUSD", 2, -10.0, "2019-04-30 00:00:00")
    window(c, f"{ROOT}_1d", "ETHUSD", 2, 0.0, "2019-04-30 00:00:00")
    w(c / f"05_verification/x_run/verdicts/{ROOT}_1d/result.json",
      {"status": "confirmed", "main_measure": {"name": "slope", "statistic": {"name": "OLS slope t", "value": 3.1}},
       "decided_by": "t >= 2", "situation_check": {"agreement": 0.97, "passed": True}, "supporting_check": {"name": "mean > 0", "passed": True}, "counts": {"cases": 300}})
    w(c / f"06_profitability/x_run/checks/{ROOT}_1d/result.json",
      {"status": "not profitable enough", "decided_by": "failed: Calmar",
       "measures": [{"measure": "sharpe_min", "label": "Sharpe", "value": 0.5, "threshold": 0, "comparison": "above", "passed": True},
                    {"label": "Calmar", "value": 0.2, "threshold": 0.75, "comparison": "above", "passed": False}]})
    w(c / f"07d_not_profitable/x_run/{ROOT}_1d/result.json",
      {"line": "7.d", "findings": {"F1": "a finding"}, "ideas": [{"name": "Fall rebounds", "idea": "A fall rebounds."}],
       "idea_ids": [WAITING], "no_ideas": None})
    w(c / "orchestration/run_idea/x_run/journal.jsonl", "\n".join(json.dumps(j) for j in [
        {"backtest": f"{ROOT}_1d", "step": "step3_plan", "action": "called", "usd": 0.1, "seconds": 20},
        {"backtest": f"{ROOT}_1d", "step": "step5_verdict", "action": "called", "usd": 0.2, "seconds": 30},
        {"backtest": f"{ROOT}_1d", "step": "step7_7.a", "action": "called: not run: entry condition", "usd": 0,
         "seconds": 0.5},
        {"backtest": f"{CHILD}_1d", "step": "step3_plan", "action": "called", "usd": 0.05, "seconds": 10}]) + "\nnot json\n")
    w(c / "orchestration/run_brief/x_run/journal.jsonl", json.dumps({"step": "step2_ideas", "usd": 0.04, "seconds": 12}))
    w(c / "orchestration/loop/x_run/loop.jsonl", json.dumps({"turn": 1, "idea": ROOT, "why": "rank 1"}))
    w(c / "orchestration/loop/x_run/queue.json", [{"idea": WAITING, "status": "candidate", "score": 0.2}])
    return c


def the_run(cards):
    data = bp.build(cards)
    assert [r["name"] for r in data["runs"]] == ["x_run"]
    return data["runs"][0]


def test_steps_read_from_their_own_files(cards):
    r = the_run(cards)
    b = r["backtests"][f"{ROOT}_1d"]
    assert b["step3"]["outcome"] == "plan" and b["step3"]["fit"] == "exact"
    assert b["step5"]["status"] == "confirmed" and b["step5"]["t"] == 3.1 and b["step5"]["counts"] == {"cases": 300}
    assert b["step5"]["situation"] == 0.97 and b["step5"]["situation_passed"] is True
    assert b["step6"]["status"] == "not profitable enough" and b["step6"]["failed"] == ["Calmar"]
    assert b["step7"][0]["line"] == "7.d" and b["step7"][0]["ideas"][0]["id"] == WAITING
    refused = r["backtests"][f"{CHILD}_1d"]["step3"]
    assert refused["outcome"] == "missing-components"
    assert refused["reason"] == "No component reads volume.\nIt stops here."
    assert "INDEX" not in " ".join(r["backtests"])


def test_book_is_chained_in_time_order_mean_over_coins(cards):
    book = the_run(cards)["backtests"][f"{ROOT}_1d"]["book"]
    assert book["windows"] == ["w2", "w1"]                      # w2 ends first
    assert book["values"] == [1.0, pytest.approx(0.95), pytest.approx(0.95 * 1.15)]
    assert book["years"] == ["2019", "2021"] and book["coins"] == ["BTCUSD", "ETHUSD"] and book["coin_windows"] == 4


def test_tree_follows_the_ids(cards):
    r = the_run(cards)
    assert r["roots"] == [ROOT]
    assert r["ideas"][ROOT]["children"] == [CHILD, WAITING]
    assert r["ideas"][CHILD]["line"] == "7.b" and r["ideas"][WAITING]["line"] == "7.g"
    assert r["ideas"][WAITING]["queue"] == {"status": "candidate", "score": 0.2} and r["ideas"][WAITING]["backtests"] == []
    assert r["ideas"][ROOT]["statement"] == "A rise continues."
    # bar size: from the backtest's id when tested, else from the idea file's bar: line
    assert r["ideas"][ROOT]["bars"] == ["1d"] and r["ideas"][CHILD]["bars"] == ["1d"] and r["ideas"][WAITING]["bars"] == ["4h"]
    assert r["ideas"][ROOT]["turn"] == {"turn": 1, "why": "rank 1"}


def test_counts_and_sums(cards):
    t = the_run(cards)["totals"]
    assert t["step3"] == {"plan": 1, "missing-components": 1}
    assert t["step5"] == {"confirmed": 1} and t["step6"] == {"not profitable enough": 1}
    assert t["bars"] == {"1d": 2}                                          # the bar size from each backtest's id
    assert t["usd"] == pytest.approx(0.39) and t["seconds"] == pytest.approx(72.5, abs=0.5) and t["turns"] == 1
    cost = the_run(cards)["backtests"][f"{ROOT}_1d"]["cost"]
    assert cost == {"step3_plan": {"usd": 0.1, "seconds": 20.0, "ran": True},
                    "step5_verdict": {"usd": 0.2, "seconds": 30.0, "ran": True},
                    "step7_7.a": {"usd": 0.0, "seconds": 0.5, "ran": False}}
    # every idea in exactly one state
    assert t["idea_states"] == {"backtested": 1, "blocked at step 3": 1, "waiting in the queue": 1}


def test_key_figures_and_depth(cards):
    data = bp.build(cards)
    r = data["runs"][0]
    t = r["totals"]
    assert r["backtests"][f"{ROOT}_1d"]["step6"]["sharpe"] == 0.5          # the measure sharpe_min, by its id
    assert t["best_t"] == {"confirmed": 3.1} and t["best_sharpe"] == {"not profitable enough": 0.5}
    # level = generations below the brief, from the id; ideas counted once, whatever their backtests
    assert t["levels"] == [{"level": 1, "ideas": 1, "tested": 1}, {"level": 2, "ideas": 2, "tested": 0}]
    assert data["lines"] == {"7.d": "not profitable"}                      # from the folder 07d_not_profitable


def test_best_is_the_largest_per_status():
    bts = {"a": {"step5": {"status": "confirmed", "t": 2.5}}, "b": {"step5": {"status": "confirmed", "t": 4.0}},
           "c": {"step5": {"status": "rejected", "t": -3.0}}, "d": {"step5": {"status": "mismatch", "t": None}},
           "e": {"step5": None}}
    assert bp.best(bts, "step5", "t") == {"confirmed": 4.0, "rejected": -3.0}


def test_per_coin_rows_and_when_it_ran(cards):
    book = the_run(cards)["backtests"][f"{ROOT}_1d"]["book"]
    assert book["fields"][0] == "net_return_pct"
    assert book["per_coin"]["ETHUSD"] == [[0.0, 2, 50.0, -2.0, 1.0, 30.0], [20.0, 1, 50.0, -2.0, 1.0, 30.0]]
    assert book["ran"] == "2026-11-17 01:00"


def test_briefs_are_found_by_the_idea_number(cards):
    data = bp.build(cards)
    assert list(data["briefs"]) == ["001"]                       # INDEX.md is not a brief
    assert data["briefs"]["001"]["title"] == "rises continue" and data["briefs"]["001"]["runs"] == ["x_run"]
    r = data["runs"][0]
    assert {i["brief"] for i in r["ideas"].values()} == {"001"}


def test_dates_come_from_the_record(cards):
    # without dated journal lines: the backtest engine's own run times (manifest created_utc of w1 and w2)
    r = the_run(cards)
    assert r["dates"] == ["2026-11-17 01:00", "2026-11-17 02:00"]
    assert r["ideas"][ROOT]["dated"] == "2026-11-17 01:00" and r["ideas"][CHILD]["dated"] is None
    # a journal dated in full counts; a time without its day does not
    w(cards / "orchestration/run_idea/x_run/journal.jsonl", "\n".join(json.dumps(j) for j in [
        {"at": "00:30:00 UTC", "backtest": f"{ROOT}_1d", "step": "step3_plan", "action": "called"},
        {"at": "2026-11-16T23:59:00Z", "backtest": f"{CHILD}_1d", "step": "step3_plan", "action": "called"},
        {"at": "2026-11-17T05:10:00Z", "backtest": f"{ROOT}_1d", "step": "step5_verdict", "action": "called"}]))
    r = the_run(cards)
    assert r["dates"] == ["2026-11-16 23:59", "2026-11-17 05:10"]
    assert r["ideas"][CHILD]["dated"] == "2026-11-16 23:59" and r["ideas"][ROOT]["dated"] == "2026-11-17 05:10"
    assert bp.stamp("00:30:00 UTC") is None and bp.stamp("2026-11-17T05:10:00+00:00") == "2026-11-17 05:10"


def test_a_backtest_folder_gives_where_its_chart_files_are(cards):
    # the page reads the committed names there, then the .local ones; a plan without a backtest has no place to look
    r = the_run(cards)
    assert r["backtests"][f"{ROOT}_1d"]["chart"] == f"04_backtest/x_run/backtests/{ROOT}_1d/"
    assert r["backtests"][f"{CHILD}_1d"]["chart"] is None


def test_run_brief_and_purpose(cards):
    r = the_run(cards)
    assert r["run_brief"] == "X_RUN.md" and r["purpose"] == "See whether rises continue."
    w(cards / "02_ideation/x_more_run/ideas/002-01_y.md", "Idea: y\n")
    assert bp.run_brief_file(cards, "x_more_run").name == "X_RUN.md"   # the longest name the run starts with
    assert bp.run_brief_file(cards, "xy_run") is None


def test_missing_files_are_not_a_failure(cards):
    (cards / f"05_verification/x_run/verdicts/{ROOT}_1d/result.json").write_text("{broken", encoding="utf-8")
    (cards / "orchestration/loop/x_run/queue.json").unlink()
    r = the_run(cards)
    assert r["backtests"][f"{ROOT}_1d"]["step5"] is None
    assert r["backtests"][f"{CHILD}_1d"]["book"] is None


def test_page_holds_the_data_and_writes_only_its_file(cards, tmp_path, monkeypatch):
    out = tmp_path / "out" / "runs.html"
    out.parent.mkdir()
    before = {p for p in cards.rglob("*")}
    monkeypatch.setattr(sys, "argv", ["build_page.py", "--cards", str(cards), "--out", str(out)])
    bp.main()
    after = {p for p in cards.rglob("*")}
    assert after - before == {out}
    html = out.read_text(encoding="utf-8")
    assert "/*DATA*/null" not in html and '"name":"x_run"' in html
