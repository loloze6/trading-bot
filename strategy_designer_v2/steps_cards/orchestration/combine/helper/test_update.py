"""Steps 10 to 12 (update.py, final_test.py) on hand-made records: a changed list of candidates builds a version, an
unchanged one does not, readiness against holding, the final test's refusals and its record written before the run."""
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import boxes as bx  # noqa: E402
import combine as cb  # noqa: E402
import update as up  # noqa: E402
import final_test as ft  # noqa: E402

COINS = ["AUSD", "BUSD"]
N = 1500
OLD_INDEX = ("# Portfolio versions (every version tried stays listed)\n\n| Version | Commit | Books | In-sample | Unseen coins |\n"
             "|---|---|---|---|---|\n| v2b | b30c67e224 | 10 books | in-sample Sharpe 2.055 | unseen coins Sharpe 1.008 |\n")


def closes(seed, drift=0.0, vol=0.03):
    rng = np.random.default_rng(seed)
    return 100 * np.cumprod(1 + drift + vol * rng.standard_normal(N))


@pytest.fixture
def world(tmp_path, monkeypatch):
    """A repository in miniature: two coins' daily files, an empty register, the old INDEX with v2b."""
    days = pd.date_range("2019-01-01", periods=N, freq="D")
    data = tmp_path / "data"; data.mkdir()
    close = {c: closes(i, drift=0.001, vol=0.02) for i, c in enumerate(COINS)}
    for c in COINS:
        pd.DataFrame({"timestamp": days.strftime("%Y-%m-%d"), "close": close[c]}).to_csv(data / f"kraken_{c}_1d.csv", index=False)
    func = tmp_path / "orchestration" / "combine"; (func / "portfolios").mkdir(parents=True)
    (func / "portfolios" / "INDEX.md").write_text(OLD_INDEX)
    reg = tmp_path / "register"; reg.mkdir()
    (reg / "books.json").write_text("[]")
    monkeypatch.setattr(cb, "STEPS", tmp_path); monkeypatch.setattr(cb, "FUNC", func); monkeypatch.setattr(cb, "REG", reg)
    monkeypatch.setattr(up, "PORTFOLIOS", func / "portfolios"); monkeypatch.setattr(ft, "MARKS", func / "final_tests")
    monkeypatch.setattr(up.bx, "DATA", data)
    bx.profiles.cache_clear()
    return {"root": tmp_path, "days": days, "data": data, "close": close, "reg": reg, "func": func}


def chart(w, records, run, rid, value, coins=COINS):
    """A hand-made chart file: long on every day, its value as given per coin."""
    d = w["root"] / "04_backtest" / run / records / "backtests" / rid; d.mkdir(parents=True, exist_ok=True)
    pd.concat([pd.DataFrame({"coin": c, "window": "w1", "timestamp": w["days"].strftime("%Y-%m-%d"), "close": w["close"][c],
                             "forecast": 0.0, "position": 0.5, "value": value(c)}) for c in coins]).to_csv(d / "chart_bars.csv.gz", index=False)


def add_book(w, n, kind="paying", common=True, value=None):
    """Register book n (its own family), with its common record unless common=False."""
    run, rid = "x_run", f"{n:03d}-01_book-{n}_1d"
    rng = np.random.default_rng(100 + n)
    value = value or (lambda c: 1000 * np.cumprod(1 + 0.002 + 0.01 * rng.standard_normal(N)))
    if common:
        chart(w, "common", run, rid, value)
        j = w["root"] / "orchestration" / "common_record" / run; j.mkdir(parents=True, exist_ok=True)
        (j / f"{rid}.json").write_text("{}")
    books = json.loads((w["reg"] / "books.json").read_text())
    books.append({"key": f"{run}__{rid}", "run": run, "id": rid, "kind": kind, "side": "long", "made_utc": f"2026-11-0{n}T00:00:00"})
    (w["reg"] / "books.json").write_text(json.dumps(books))
    return f"{run}__{rid}"


def test_no_common_record_builds_nothing(world):
    add_book(world, 1, common=False)
    add_book(world, 2, kind="confirmed")
    before = sorted(p.relative_to(world["func"]) for p in world["func"].rglob("*"))
    name, why = up.update(world["data"])
    assert name is None and "no candidate" in why
    assert (world["func"] / "portfolios" / "INDEX.md").read_text() == OLD_INDEX          # byte-identical
    assert sorted(p.relative_to(world["func"]) for p in world["func"].rglob("*")) == before


def test_a_changed_list_builds_the_next_version_and_an_unchanged_one_does_not(world):
    a, b = add_book(world, 1), add_book(world, 2)
    add_book(world, 3, kind="confirmed")                    # confirmed only: not a candidate
    name, m = up.update(world["data"])
    assert name == "v3"                                     # after v2b
    p = json.loads((world["func"] / "portfolios" / "v3" / "portfolio.json").read_text())
    assert p["candidates"] == sorted([a, b]) and p["records"] == "common"
    assert {x["key"] for x in p["books"]} == {a, b}         # two families, unrelated: both kept
    assert (world["func"] / "portfolios" / "v3" / "boxes.csv").exists()
    idx = (world["func"] / "portfolios" / "INDEX.md").read_text()
    assert idx.startswith(OLD_INDEX) and up.SECTION in idx and "| v3 |" in idx

    snapshot = idx
    name, why = up.update(world["data"])
    assert name is None and "that of v3" in why
    assert (world["func"] / "portfolios" / "INDEX.md").read_text() == snapshot

    add_book(world, 4)
    name, _ = up.update(world["data"])
    assert name == "v4"
    assert len(json.loads((world["func"] / "portfolios" / "v4" / "portfolio.json").read_text())["candidates"]) == 3


def test_ready_when_its_sharpe_is_above_holding(world):
    add_book(world, 1); add_book(world, 2)
    _, m = up.update(world["data"])
    v, h = m["portfolio_coins"]["this version"], m["portfolio_coins"][up.HOLDING]
    assert m["ready"] is True and v["sharpe"] > h["sharpe"]
    assert v["days"] == h["days"]                            # the same days
    assert "| ready |" in (world["func"] / "portfolios" / "INDEX.md").read_text()


def test_not_ready_when_it_earns_less_than_holding(world):
    # half the coin's move, less a cost: it earns (admitted) but its Sharpe is below holding's
    def half(c):
        r = pd.Series(world["close"][c]).pct_change().fillna(0).values
        return 1000 * np.cumprod(1 + 0.5 * r - 0.0002)
    add_book(world, 1, value=half)
    _, m = up.update(world["data"])
    assert m["portfolio_coins"]["this version"] is not None and m["ready"] is False
    assert "| not ready |" in (world["func"] / "portfolios" / "INDEX.md").read_text()


def test_holding_is_the_equal_weight_mean_of_the_coins_returns(world):
    k = add_book(world, 1)
    rows = {r["key"]: r for r in json.loads((world["reg"] / "books.json").read_text())}
    h = up.holding({k: 1.0}, rows)
    expect = pd.concat([pd.Series(world["close"][c], index=world["days"]).pct_change() for c in COINS], axis=1).mean(axis=1).dropna()
    assert np.allclose(h.values, expect.values) and len(h) == N - 1


def fake_run_book(w, seen):
    """In place of step 4: the book's chart file on the final coins, after checking the record was written first."""
    def run(r, python):
        rec = json.loads(ft.mark().read_text())
        seen.append(rec["status"])
        chart(w, ft.group(), r["run"], r["id"], lambda c: 1000 * np.cumprod(1 + 0.002 + 0.01 * np.random.default_rng(7).standard_normal(N)))
        return COINS
    return run


def test_the_final_test_refuses_a_version_not_ready_and_a_used_group(world, monkeypatch):
    def half(c):
        r = pd.Series(world["close"][c]).pct_change().fillna(0).values
        return 1000 * np.cumprod(1 + 0.5 * r - 0.0002)
    add_book(world, 1, value=half)
    up.update(world["data"])                                 # v3, not ready
    with pytest.raises(SystemExit, match="not ready"):
        ft.final_test("v3", "python3", run_book=fake_run_book(world, []))
    with pytest.raises(SystemExit, match="no measures.json"):
        ft.final_test("v2b", "python3", run_book=fake_run_book(world, []))
    assert not ft.mark().exists()

    add_book(world, 2); add_book(world, 3)
    up.update(world["data"])                                 # v4
    assert json.loads((world["func"] / "portfolios" / "v4" / "measures.json").read_text())["ready"] is True
    seen = []
    rec = ft.final_test("v4", "python3", run_book=fake_run_book(world, seen))
    assert seen and set(seen) == {"started"}                 # the record existed before every run
    saved = json.loads(ft.mark().read_text())
    assert saved["status"] == "done" and saved["version"] == "v4" and saved["go"] == rec["go"]
    assert saved["measures_expected"]["step 11 on the portfolio coins"]["this version"]["sharpe"] is not None
    m = json.loads((world["func"] / "portfolios" / "v4" / "measures.json").read_text())
    assert m["final_test"]["go"] == rec["go"] and m["final_test"]["this version"]["coins"] == COINS
    assert f"| {ft.group()}: " in (world["func"] / "portfolios" / "INDEX.md").read_text()

    with pytest.raises(SystemExit, match="already made"):    # once per final group
        ft.final_test("v4", "python3", run_book=fake_run_book(world, []))


def test_a_final_test_that_fails_still_uses_the_group(world):
    add_book(world, 1); add_book(world, 2)
    up.update(world["data"])
    def broken(r, python):
        raise RuntimeError("the engine stopped")
    with pytest.raises(RuntimeError):
        ft.final_test("v3", "python3", run_book=broken)
    assert json.loads(ft.mark().read_text())["status"] == "started"
    with pytest.raises(SystemExit, match="already made"):
        ft.final_test("v3", "python3", run_book=broken)


def test_the_final_series_starts_in_2016_or_on_the_91st_day_and_ends_on_the_last_complete_day(tmp_path):
    for coin, start in (("OLD", "2014-03-01"), ("NEW", "2020-06-01")):
        d = pd.date_range(start, "2026-11-26", freq="D")
        pd.DataFrame({"timestamp": d.strftime("%Y-%m-%d"), "close": 1.0}).to_csv(tmp_path / f"kraken_{coin}USD_1d.csv", index=False)
    today = dt.date(2026, 11, 26)
    assert ft.series("OLD", tmp_path, today)["test"] == {"start": "2016-01-01", "end": "2026-11-25"}
    assert ft.series("NEW", tmp_path, today)["test"] == {"start": "2020-08-30", "end": "2026-11-25"}
