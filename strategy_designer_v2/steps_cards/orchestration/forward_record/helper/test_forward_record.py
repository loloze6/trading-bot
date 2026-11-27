"""Tests of forward_record's own logic: the start day, only days after it, lines only added, the two returns, the
frozen strategies, the guard's refusal, the coins. No backtest: the runner is replaced by a fake that writes a chart
file; the versions, plans and records are hand-made in a temporary folder."""
import gzip, json, sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forward_record as F  # noqa: E402

START = "2030-03-10"
DAYS = ["2030-03-10", "2030-03-11", "2030-03-12", "2030-03-13", "2030-03-14", "2030-03-15"]


def make(tmp, weights=None):
    """A version of two strategies (run_a__s1 at 0.5, run_a__s2 at 1.0), their plans, configs and common results."""
    weights = weights or {"run_a__s1": 0.5, "run_a__s2": 1.0}
    steps, ports = tmp / "steps", tmp / "portfolios"
    for key in weights:
        run, rid = key.split("__")
        plans = steps / "03_test_plan" / run / "plans"; plans.mkdir(parents=True, exist_ok=True)
        (plans / f"{rid}.md").write_text(f"---\ndata-bar: 1d\n---\nplan {rid}\n")
        (plans / f"{rid}_config.json").write_text(json.dumps({"id": rid}))
        res = steps / "orchestration" / "common_record" / run; res.mkdir(parents=True, exist_ok=True)
        (res / f"{rid}.json").write_text(json.dumps({"plan": f"03_test_plan/{run}/plans/{rid}.md"}))
    (ports / "vT").mkdir(parents=True)
    (ports / "vT" / "portfolio.json").write_text(json.dumps({
        "version": "vT", "made_utc": START + "T16:53:39Z", "commit": "abc",
        "books": [{"key": k, "weight": w} for k, w in weights.items()]}))
    return steps, ports


def chart(path, rows):
    """rows: (coin, day, close, value)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "coin,window,timestamp,close,forecast,position,value\n" + "".join(
        f"{c},w1,{d},{close},0,1,{value}\n" for c, d, close, value in rows)
    path.write_bytes(gzip.compress(text.encode()))
    return path


# value and close of each coin on each day of DAYS, per strategy
VALUES = {"run_a__s1": {"AUSD": [1000, 1010, 1010, 1020.1, 1000, 1000], "BUSD": [1000, 1000, 990, 990, 1000, 1000]},
          "run_a__s2": {"AUSD": [1000, 990, 1000, 1000, 1010, 1010]}}
CLOSES = {"AUSD": [100, 102, 101, 103, 104, 104], "BUSD": [10, 10, 11, 11, 12, 12]}
LAST = DAYS[-1]             # a window ending here writes the days up to DAYS[-2]


def fake_runner(calls, tmp, values=VALUES):
    def run_book(book, version, python, window, coin_list, engine_root, steps):
        calls.append((book["key"], dict(window["test"]), list(coin_list)))
        days = [d for d in DAYS if window["test"]["start"] <= d <= window["test"]["end"]]
        rows = [(c, d, CLOSES[c][DAYS.index(d)], v[DAYS.index(d)]) for c, v in values[book["key"]].items() for d in days]
        return chart(tmp / "engine" / book["key"] / "chart_bars.csv.gz", rows), f"{book['id']}: ran"
    return run_book


def run(tmp, steps, ports, until, calls=None, values=VALUES, guard=lambda python, window: None):
    return F.update("vT", "py", folder=tmp / "rec", until=until, portfolios=ports, steps=steps,
                    run_book=fake_runner(calls if calls is not None else [], tmp, values), guard=guard,
                    coin_list=["A", "B"])


def test_the_start_day_is_the_day_the_version_was_built_and_no_day_at_or_before_it_is_kept(tmp_path):
    steps, ports = make(tmp_path)
    r = run(tmp_path, steps, ports, LAST)
    rows = F.read_days(tmp_path / "rec" / "days.csv")
    assert r["start_day"] == START == json.loads((tmp_path / "rec" / "frozen.json").read_text())["start_day"]
    assert [x["day"] for x in rows] == DAYS[1:-1] and all(x["day"] > START for x in rows)
    # a chart that holds earlier days still gives none of them
    c = chart(tmp_path / "early.csv.gz", [("AUSD", d, 1, v) for d, v in zip(["2030-03-08", "2030-03-09"] + DAYS, range(1000, 1008))])
    kept = F.keep_forward(F.portfolio_and_holding({"k": 1.0}, {"k": c}), START)
    assert [d.strftime("%Y-%m-%d") for d in kept.index] == DAYS[1:]


def test_append_refuses_a_day_not_after_the_start_day_or_the_last_day(tmp_path):
    f = tmp_path / "days.csv"
    row = lambda d: dict.fromkeys(F.COLUMNS, 0) | {"day": d}
    for bad in (START, "2030-03-09"):
        with pytest.raises(ValueError):
            F.append(f, [row(bad)], START)
    F.append(f, [row("2030-03-12")], START)
    before = f.read_bytes()
    for bad in ("2030-03-12", "2030-03-11"):
        with pytest.raises(ValueError):
            F.append(f, [row(bad)], START)
    assert f.read_bytes() == before


def test_the_two_returns(tmp_path):
    steps, ports = make(tmp_path)
    run(tmp_path, steps, ports, LAST)
    rows = {x["day"]: x for x in F.read_days(tmp_path / "rec" / "days.csv")}
    d1 = rows["2030-03-11"]         # A: 0.5 * +1 % + 1.0 * -1 % = -0.5 %; B: 0.5 * 0 = 0; mean -0.25 %
    assert float(d1["portfolio"]) == pytest.approx(-0.0025)
    assert float(d1["holding"]) == pytest.approx((0.02 + 0.0) / 2)             # A's close +2 %, B's 0 %
    assert (d1["coins"], d1["strategies"]) == ("2", "2")
    d2 = rows["2030-03-12"]         # A: 0 + 1.0 * (1000/990 - 1); B: 0.5 * -1 %
    assert float(d2["portfolio"]) == pytest.approx(((1000 / 990 - 1) + 0.5 * -0.01) / 2)
    assert float(d2["holding"]) == pytest.approx(((101 / 102 - 1) + 0.1) / 2)


def test_an_update_only_adds_days_earlier_lines_stay_byte_for_byte(tmp_path):
    steps, ports = make(tmp_path)
    f = tmp_path / "rec" / "days.csv"
    r1 = run(tmp_path, steps, ports, "2030-03-13")
    first = f.read_bytes()
    r2 = run(tmp_path, steps, ports, LAST)
    assert (r1["days"], r2["days"]) == (2, 4) and f.read_bytes().startswith(first)
    assert (r2["last"]["added"], r2["last"]["same"], r2["last"]["different"]) == (2, 2, 0)
    r3 = run(tmp_path, steps, ports, LAST)                                      # nothing new: nothing added
    assert r3["last"]["added"] == 0 and f.read_bytes().startswith(first) and len(F.read_days(f)) == 4


def test_the_windows_last_day_waits_for_the_next_update(tmp_path):
    """The engine closes every position on a window's last bar: that day's return holds a cost the portfolio would
    not pay, so it is written only once a later day is the window's last."""
    steps, ports = make(tmp_path)
    f = tmp_path / "rec" / "days.csv"
    assert run(tmp_path, steps, ports, "2030-03-11")["days"] == 0               # one complete day: it waits
    run(tmp_path, steps, ports, "2030-03-12")
    assert [x["day"] for x in F.read_days(f)] == ["2030-03-11"]
    run(tmp_path, steps, ports, "2030-03-14")
    assert [x["day"] for x in F.read_days(f)] == ["2030-03-11", "2030-03-12", "2030-03-13"]


def test_an_earlier_day_computed_differently_is_shown_and_not_rewritten(tmp_path):
    steps, ports = make(tmp_path)
    f = tmp_path / "rec" / "days.csv"
    run(tmp_path, steps, ports, "2030-03-13")
    first = f.read_bytes()
    other = {**VALUES, "run_a__s2": {"AUSD": [1000, 950, 1000, 1000, 1010, 1010]}}
    r = run(tmp_path, steps, ports, LAST, values=other)
    assert f.read_bytes().startswith(first)
    assert r["last"]["different"] == 2 and r["last"]["first_different"] == "2030-03-11"
    assert "2 different" in (tmp_path / "rec" / "record.md").read_text()


def test_no_forward_day_yet_no_run_and_an_empty_file(tmp_path):
    steps, ports = make(tmp_path)
    calls = []
    r = run(tmp_path, steps, ports, START, calls)
    assert calls == [] and r["days"] == 0 and r["last"] is None
    assert (tmp_path / "rec" / "days.csv").read_text() == ",".join(F.COLUMNS) + "\n"
    assert "no forward day is complete yet" in (tmp_path / "rec" / "record.md").read_text()


def test_a_strategy_that_is_no_longer_the_frozen_one_stops_the_update(tmp_path):
    steps, ports = make(tmp_path)
    run(tmp_path, steps, ports, "2030-03-13")
    before = (tmp_path / "rec" / "days.csv").read_bytes()
    (steps / "03_test_plan/run_a/plans/s1_config.json").write_text(json.dumps({"id": "s1", "edited": True}))
    calls = []
    with pytest.raises(SystemExit) as e:
        run(tmp_path, steps, ports, LAST, calls)
    assert "run_a__s1" in str(e.value) and calls == []
    assert (tmp_path / "rec" / "days.csv").read_bytes() == before
    # the weights are the frozen ones too: a version file rewritten later changes nothing
    frozen = json.loads((tmp_path / "rec" / "frozen.json").read_text())
    assert [b["weight"] for b in frozen["books"]] == [0.5, 1.0]


def test_the_guards_refusal_stops_before_any_run_with_its_message(tmp_path):
    steps, ports = make(tmp_path)
    calls = []
    with pytest.raises(SystemExit) as e:
        run(tmp_path, steps, ports, "2030-03-14", calls, guard=lambda python, window: "refused (dates withheld)")
    assert "refused (dates withheld)" in str(e.value) and calls == []
    assert F.read_days(tmp_path / "rec" / "days.csv") == []


def test_sharpe_only_from_60_days():
    few = F.stats([0.01, -0.005] * 29)
    enough = F.stats([0.01, -0.005] * 30)
    assert few["days"] == 58 and few["sharpe"] is None and enough["sharpe"] is not None
    s = F.stats([0.10, -0.50, 0.10])
    assert s["return"] == pytest.approx(1.1 * 0.5 * 1.1 - 1) and s["worst_fall"] == pytest.approx(0.5)
    assert F.stats([-0.10])["worst_fall"] == pytest.approx(0.10)               # a fall from the start counts
    frozen = {"version": "vT", "made_utc": START + "T00:00:00Z", "version_commit": "abc", "start_day": START, "books": []}
    rows = [{"day": "2030-03-11", "portfolio": "0.01", "holding": "-0.02"}]
    assert "too few days" in F.record_text(frozen, rows)


def test_the_last_tests_coins_are_never_read(tmp_path, monkeypatch):
    """data_use.md: the final group is used by no step until the final test. The coins run and the coins whose data
    is extended are the portfolio group; the helper's code never names the final group."""
    steps, ports = make(tmp_path)
    calls, asked = [], []
    monkeypatch.setattr(F, "extend_data", lambda python, coin_list: asked.append(list(coin_list)) or "")
    monkeypatch.setattr(F, "last_complete_day", lambda coin_list, data=None: asked.append(list(coin_list)) or DAYS[-1])
    F.update("vT", "py", update_data=True, folder=tmp_path / "rec", portfolios=ports, steps=steps,
             run_book=fake_runner(calls, tmp_path, {k: {} for k in VALUES}), guard=lambda p, w: None)
    final = set(F.coins.FINAL)
    assert asked and calls and all(c == F.coins.portfolio_group() for c in asked + [c for _, _, c in calls])
    assert not final & set(F.coins.portfolio_group())
    text = Path(F.__file__).read_text()
    assert "FINAL" not in text and not any(f"{c}USD" in text for c in final)
    cmd = []
    monkeypatch.undo()
    monkeypatch.setattr(F.subprocess, "run", lambda c, **k: cmd.append(c) or type("R", (), {"stdout": "", "stderr": ""})())
    F.extend_data("py", F.coins.portfolio_group())
    assert cmd[0][cmd[0].index("--coins") + 1:] == F.coins.portfolio_group()   # the tool gets the coins by name
