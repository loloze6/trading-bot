"""Tests of make_assessment on hand-made records (not market data): the numbers are recomputed here independently,
and the status follows the rule. Run: python -m pytest test_make_assessment.py -q"""
import gzip, json, math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

import make_assessment as m

RULE = yaml.safe_load((Path(m.__file__).parent / "rule.yaml").read_text())


def write_record(root, books, closes, trades_per_window=5, forced_last=True):
    """books/closes: {coin: [array of daily values per window]}. One bar per day."""
    for coin in books:
        for k, (b, c) in enumerate(zip(books[coin], closes[coin]), 1):
            d = root / coin / f"w{k}"
            d.mkdir(parents=True)
            ts = pd.date_range(f"2001-0{k}-01", periods=len(b), freq="D")
            pd.DataFrame({"timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"), "close": c, "postRebalance_total_value": b}).to_csv(
                d / "bars.csv.gz", index=False, compression="gzip")
            exits = [ts[i].isoformat() for i in range(1, 1 + trades_per_window)]
            if forced_last:
                exits.append(ts[-1].isoformat())
            with gzip.open(d / "trades.json.gz", "wt") as g:
                json.dump([{"exit_time": e} for e in exits], g)


def independent(books, closes):
    """The same definitions, written again without the helper: equal-weight daily returns per window."""
    r, h = [], []
    for k in range(len(next(iter(books.values())))):
        r += list(np.mean([np.diff(books[c][k]) / books[c][k][:-1] for c in books], axis=0))
        h += list(np.mean([np.diff(closes[c][k]) / closes[c][k][:-1] for c in closes], axis=0))
    s = lambda x: np.mean(x) / np.std(x, ddof=1) * math.sqrt(365)
    return np.array(r), np.array(h), s


def test_a_steady_book_is_worth_acting_on(tmp_path):
    rng = np.random.default_rng(1)
    books = {c: [1000 * np.cumprod(1 + 0.002 + rng.normal(0, 0.005, 60)) for _ in range(3)] for c in ("AAA", "BBB")}
    closes = {c: [100 * np.cumprod(1 + rng.normal(0, 0.03, 60)) for _ in range(3)] for c in ("AAA", "BBB")}
    write_record(tmp_path, books, closes)
    rows, facts = m.assess(tmp_path, RULE)
    v = {x["bar"]: x["value"] for x in rows}
    r, h, s = independent(books, closes)
    assert v["sharpe_min"] == pytest.approx(s(r))
    assert v["sharpe_vs_hold_min"] == pytest.approx(s(r) - s(h))
    assert v["avg_daily_return_min"] == pytest.approx(r.mean())
    assert facts["trades"] == 2 * 3 * 5            # the forced close on each window's last bar is not counted
    assert v["trade_frequency_min"] == pytest.approx(30 / (2 * 3 * 60))
    assert all(x["passed"] for x in rows)


def test_a_losing_book_is_not_worth_acting_on(tmp_path):
    rng = np.random.default_rng(2)
    books = {c: [1000 * np.cumprod(1 - 0.001 + rng.normal(0, 0.01, 60)) for _ in range(3)] for c in ("AAA",)}
    closes = {c: [100 * np.cumprod(1 + rng.normal(0, 0.03, 60)) for _ in range(3)] for c in ("AAA",)}
    write_record(tmp_path, books, closes)
    rows, _ = m.assess(tmp_path, RULE)
    passed = {x["bar"]: x["passed"] for x in rows}
    assert not passed["sharpe_min"] and not passed["avg_daily_return_min"]


def test_one_bad_window_fails_leave_one_out_and_calmar(tmp_path):
    good = 1000 * np.cumprod(np.full(60, 1.003))
    bad = 1000 * np.cumprod(np.full(60, 0.97))      # one window loses heavily
    up = 1000 * np.cumprod(np.full(60, 1.0005))
    books = {"AAA": [good, bad, up]}
    closes = {"AAA": [up, up, up]}
    write_record(tmp_path, books, closes)
    rows, facts = m.assess(tmp_path, RULE)
    v = {x["bar"]: x for x in rows}
    r, _, s = independent(books, closes)
    curve = np.cumprod(1 + r)
    fall = np.max(1 - curve / np.maximum.accumulate(np.concatenate([[1.0], curve]))[1:])
    assert facts["deepest_fall"] == pytest.approx(fall)
    assert not v["calmar_min"]["passed"]
    assert v["leave_one_window_out_sharpe_min"]["value"] == pytest.approx(min(
        s(np.concatenate([np.diff(b) / b[:-1] for j, b in enumerate(books["AAA"]) if j != i])) for i in range(3)))


def test_too_few_trades_fails_the_frequency_bar(tmp_path):
    rng = np.random.default_rng(3)
    books = {"AAA": [1000 * np.cumprod(1 + 0.002 + rng.normal(0, 0.004, 120)) for _ in range(2)]}
    closes = {"AAA": [100 * np.cumprod(1 + rng.normal(0, 0.03, 120)) for _ in range(2)]}
    write_record(tmp_path, books, closes, trades_per_window=0)
    rows, _ = m.assess(tmp_path, RULE)
    assert not {x["bar"]: x["passed"] for x in rows}["trade_frequency_min"]
