"""ideas_similarities_check on books whose answer is known by construction (no backtest, no model call)."""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ideas_similarities_check as pb  # noqa: E402
import book_returns as br  # noqa: E402

rng = np.random.default_rng(7)
DAYS = pd.date_range("2020-01-01", periods=800, freq="D", tz="UTC")


def s(values, index=DAYS):
    return pd.Series(values, index=index)


def test_a_copy_is_fully_explained_on_the_same_period():
    x = s(rng.normal(0, 0.01, len(DAYS)))
    c = pb.compare(x, x, 24)
    assert c["comparable"] and c["share_explained"] == pytest.approx(1.0) and c["who_leads"] == "same period"
    assert c["direction"] == "+" and c["what_is_left"] == pytest.approx(0.0, abs=1e-12)


def test_the_same_book_one_period_later_reads_behind_and_one_earlier_reads_ahead():
    x = rng.normal(0, 0.01, len(DAYS) + 1)
    other = s(x[1:])                       # other[t] = x[t+1]: the other acts one period before the new book
    new = s(x[:-1])                        # new[t] = x[t]
    c = pb.compare(new, other, 24)         # new[t] = other[t-1]: the new book one period behind
    assert c["who_leads"] == "new one period behind" and c["share_explained"] == pytest.approx(1.0)
    c = pb.compare(other, new, 24)
    assert c["who_leads"] == "new one period ahead" and c["share_explained"] == pytest.approx(1.0)


def test_the_opposite_book_is_the_same_effect_with_direction_minus():
    x = s(rng.normal(0, 0.01, len(DAYS)))
    c = pb.compare(-x + 0.001, x, 24)
    assert c["share_explained"] == pytest.approx(1.0) and c["direction"] == "-"
    assert c["what_is_left"] == pytest.approx(0.001)


def test_noise_explains_about_nothing_and_what_is_left_is_the_mean():
    a = s(rng.normal(0.002, 0.01, len(DAYS)))
    b = s(rng.normal(0, 0.01, len(DAYS)))
    c = pb.compare(a, b, 24)
    assert c["share_explained"] < 0.02 and c["what_is_left"] == pytest.approx(a.mean(), abs=5e-4) and c["what_is_left_t"] > 3


def test_under_one_year_in_common_is_not_comparable_and_only_common_periods_count():
    a = s(rng.normal(0, 0.01, len(DAYS)))
    b = a.iloc[:300]                                        # 300 days in common
    c = pb.compare(a, b, 24)
    assert not c["comparable"] and c["window_in_common"]["periods"] == 300
    new = a.copy(); new.iloc[400:] = rng.normal(0, 0.5, len(DAYS) - 400)      # wild returns the other book never ran
    c = pb.compare(new, a.iloc[:400], 24)
    assert c["comparable"] and c["share_explained"] == pytest.approx(1.0)   # only the 400 periods in common count


def test_hours_set_the_span():
    hours = pd.date_range("2020-01-01", periods=24 * 200, freq="h", tz="UTC")   # 200 days of hourly periods
    x = pd.Series(rng.normal(0, 0.01, len(hours)), index=hours)
    assert not pb.compare(x, x, 1)["comparable"]


def test_the_comparison_timeframe_is_the_larger_bar():
    assert pb.larger("1h", "1h") == "1h" and pb.larger("1h", "4h") == "4h" and pb.larger("4h", "1d") == "1d"
    assert br.timeframes_from("1h") == ["1h", "4h", "1d"] and br.timeframes_from("1d") == ["1d"]


def write_window(path, ts, close, value):
    path.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"timestamp": ts.strftime("%Y-%m-%d %H:%M:%S+00:00"), "close": close,
                  "postRebalance_total_value": value}).to_csv(path / "bars.csv.gz", index=False)


def test_book_returns_per_period_inside_each_window(tmp_path):
    rec = tmp_path / "x_1h"
    ts = pd.date_range("2024-01-01", periods=48, freq="h", tz="UTC")
    value = 1000 * np.cumprod(np.full(48, 1.001))
    write_window(rec / "BTCUSD" / "w1", ts, np.full(48, 100.0), value)
    write_window(rec / "ETHUSD" / "w1", ts, np.full(48, 100.0), np.full(48, 1000.0))
    d = br.book_returns(rec, "1d")
    assert len(d) == 1                                          # two days in the window: one return between them
    assert d["book"].iloc[0] == pytest.approx((1.001 ** 24 - 1) / 2)   # each coin's day first, then their mean
    h = br.book_returns(rec, "1h")
    assert len(h) == 47 and h["book"].iloc[0] == pytest.approx(0.0005)


def test_a_record_that_is_not_paying_is_refused(tmp_path):
    with pytest.raises(SystemExit):
        pb.add(tmp_path / "x_1d", "nope_run", root=tmp_path / "register", steps=tmp_path)


def test_the_chart_file_stands_in_for_bars_that_are_not_on_this_machine(tmp_path):
    ts = pd.date_range("2024-01-01", periods=72, freq="h", tz="UTC")
    value = 1000 * np.cumprod(1 + rng.normal(0, 0.002, 72)); close = 100 * np.cumprod(1 + rng.normal(0, 0.01, 72))
    a = tmp_path / "a_1h"; write_window(a / "BTCUSD" / "w1", ts, close, value)
    b = tmp_path / "b_1h"; b.mkdir()
    pd.DataFrame({"coin": "BTCUSD", "window": "w1", "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S+00:00"), "close": close,
                  "forecast": 0.0, "position": 0.0, "value": value}).to_csv(b / "chart_bars.csv.gz", index=False)
    pd.testing.assert_frame_equal(br.book_returns(a, "4h"), br.book_returns(b, "4h"))


def make_book(steps, run, rid, s5, s6, value):
    rec = steps / "04_backtest" / run / "backtests" / rid
    ts = pd.date_range("2020-01-01", periods=len(value), freq="D", tz="UTC")
    write_window(rec / "BTCUSD" / "w1", ts, np.full(len(value), 100.0), value)
    (rec / "BTCUSD" / "w1" / "manifest.json").write_text(json.dumps({"git_sha": "abc", "created_utc": "2026-11-22T00:00:00"}))
    for step, folder, st in ((5, "05_verification/{}/verdicts", s5), (6, "06_profitability/{}/checks", s6)):
        d = steps / folder.format(run) / rid; d.mkdir(parents=True, exist_ok=True)
        (d / "result.json").write_text(json.dumps({"status": st}))
    return rec


def test_confirmed_books_are_compared_with_the_paying_books_and_a_repair_with_its_parent(tmp_path):
    """Operator, 2026-11-22: the register holds paying and confirmed books; a book's nearest relative is a paying book; a
    repair (line 7.d's idea) is also compared with the idea it repairs; a paying book is not compared with confirmed ones."""
    steps, reg = tmp_path / "steps", tmp_path / "register"
    n = 500; x, y = rng.normal(0, 0.01, n), rng.normal(0, 0.01, n)
    curve = lambda r: 1000 * np.cumprod(1 + r)
    run = "t_run"
    pb.add(make_book(steps, run, "p-01_pay_1d", "confirmed", "profitable enough", curve(x)), run, root=reg, steps=steps)
    pb.add(make_book(steps, run, "c-01_real_1d", "confirmed", "not profitable enough", curve(y)), run, root=reg, steps=steps)
    pb.add(make_book(steps, run, "c-01_real.d1_repair_1d", "confirmed", "not profitable enough", curve(0.9 * y + 0.1 * x)), run, root=reg, steps=steps)
    with pytest.raises(SystemExit):
        pb.add(make_book(steps, run, "q-01_unclear_1d", "inconclusive", "not profitable enough", curve(x)), run, root=reg, steps=steps)
    kinds = {r["id"]: r["kind"] for r in pb.books(reg)}
    assert kinds == {"p-01_pay_1d": "paying", "c-01_real_1d": "confirmed", "c-01_real.d1_repair_1d": "confirmed"}
    assert (reg / "returns" / "t_run__p-01_pay_1d.csv.gz").exists() and (reg / "returns" / "confirmed" / "t_run__c-01_real_1d.csv.gz").exists()
    p = pb.comparison("t_run__p-01_pay_1d", reg)
    assert [o["other"]["id"] for o in p["others"]] == [] and p["parent"] is None        # paying books compare with paying books only
    r = pb.comparison("t_run__c-01_real.d1_repair_1d", reg)
    assert sorted(o["other"]["id"] for o in r["others"]) == ["c-01_real_1d", "p-01_pay_1d"]
    assert r["nearest_relative"]["other"]["id"] == "p-01_pay_1d"                      # the nearest relative is a paying book
    assert r["parent"]["other"]["id"] == "c-01_real_1d" and r["parent"]["share_explained"] > 0.9   # it kept its parent's idea


def test_the_matrix_holds_every_pair_of_paying_books_with_similar_books_together(tmp_path):
    """Operator, 2026-11-22 (topic 44): every paying book and its similarity to every other; a family shows as a block."""
    steps, reg = tmp_path / "steps", tmp_path / "register"
    n = 500; a, b = rng.normal(0, 0.01, n), rng.normal(0, 0.01, n)
    curve = lambda r: 1000 * np.cumprod(1 + r)
    run = "m_run"
    for rid, r in (("a1_x_1d", a), ("b1_y_1d", b), ("a2_x-copy_1d", a + rng.normal(0, 0.001, n)), ("c1_real_1d", b)):
        kind = ("confirmed", "not profitable enough") if rid.startswith("c1") else ("confirmed", "profitable enough")
        pb.add(make_book(steps, run, rid, *kind, curve(r)), run, root=reg, steps=steps)
    for r in pb.books(reg):
        pb.write_comparison(r["key"], reg)
    pb.write_summary(reg)
    order, cell = pb.matrix(reg)
    ids = [r["id"] for r in order]
    assert ids == ["a1_x_1d", "a2_x-copy_1d", "b1_y_1d"]                 # paying books only; the copy next to its original
    assert cell[("m_run__a1_x_1d", "m_run__a2_x-copy_1d")]["share_explained"] > 0.95
    text = (reg / "MATRIX.md").read_text(); csv = (reg / "matrix.csv").read_text().splitlines()
    assert "| **1** | · |" in text and len(csv) == 1 + 3 * 2                   # header and every ordered pair


def test_periods_are_utc_seconds_whatever_unit_pandas_stores():
    """Night 5: pandas 3 stores times in microseconds; the periods must still be seconds (and read back the same)."""
    t = pd.Series(pd.to_datetime(["2022-01-02 00:00", "2022-01-02 01:00"], utc=True))
    for unit in ("ns", "us", "s"):
        s = pb.utc_seconds(t.astype(f"datetime64[{unit}, UTC]"))
        assert list(s) == [1641081600, 1641085200]
        assert list(pd.to_datetime(s, unit="s", utc=True)) == list(t)
