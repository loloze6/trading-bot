"""idea_size.py on a record whose answer is known by construction."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from idea_size import size  # noqa: E402
import pandas as pd


def write_window(path, close, fc, alloc, value=None):
    """One window of hourly bars. Without a value series, the book's value follows the book without costs."""
    close = np.asarray(close, float); alloc = np.asarray(alloc, float)
    if value is None:
        r = np.append(close[1:] / close[:-1] - 1, 0.0)
        value = 1000 * np.cumprod(np.concatenate([[1.0], 1 + alloc[:-1] * r[:-1]]))
    n = len(close)
    df = pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC").strftime("%Y-%m-%d %H:%M:%S+00:00"),
                       "close": close, "forecast": fc, "previous_allocation": np.concatenate([[0.0], alloc[:-1]]),
                       "postRebalance_current_allocation": alloc, "postRebalance_total_value": value})
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(path / "bars.csv.gz", index=False)


def test_a_known_idea_size(tmp_path):
    # the coin alternates +1 % and -1 % each bar (usual move over 2 bars: known); after each signal it rises 2 % more
    n, H = 400, 2
    steps = np.array([1.01 if i % 2 else 0.99 for i in range(n)]); fc = np.zeros(n)
    for t in range(20, n - 10, 20):
        fc[t] = 5; steps[t + 1] *= 1.02
    close = 100 * np.cumprod(steps)
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, np.zeros(n))
    s = size(tmp_path / "rec", H)
    assert s["cases"] == len(range(20, n - 10, 20))
    assert s["unusual_move"] > 0.015                     # about 2 % above the coin's normal 2-bar move
    assert s["total_move"] == pytest.approx(s["unusual_move"] + s["normal_drift"], abs=1e-12)
    assert s["strength"] > 0


def test_no_signal_no_case(tmp_path):
    n = 100; write_window(tmp_path / "rec" / "BTCUSD" / "w1", np.linspace(100, 110, n), np.zeros(n), np.zeros(n))
    assert size(tmp_path / "rec", 5)["cases"] == 0


def test_the_size_t_takes_the_cases_of_one_day_together():
    """unusual_move_t: one case per day gives the ordinary t of the mean; the same cases on a second coin, the same days,
    do not make the size surer (an ordinary t would grow by about the square root of 2)."""
    from idea_size import day_t
    rng = np.random.default_rng(0)
    x = rng.normal(0.5, 2.0, 400); days = [f"d{i}" for i in range(400)]
    ordinary = x.mean() / (x.std(ddof=0) / np.sqrt(len(x)))
    assert day_t(x, days) == pytest.approx(ordinary, rel=1e-9)
    twice = day_t(np.r_[x, x], days + days)
    assert twice == pytest.approx(ordinary, rel=1e-9)                       # the same information, the same t
    assert day_t([1.0], ["d0"]) is None and day_t([1.0, 1.0], ["d0", "d1"]) is None   # one day, or no spread


def test_a_known_idea_has_a_large_t_and_two_coins_on_the_same_days_do_not_double_it(tmp_path):
    n, H = 400, 2
    steps = np.array([1.01 if i % 2 else 0.99 for i in range(n)]); fc = np.zeros(n)
    rng = np.random.default_rng(1)
    for t in range(20, n - 10, 20):
        fc[t] = 5; steps[t + 1] *= 1.02 + rng.normal(0, 0.005)
    close = 100 * np.cumprod(steps)
    write_window(tmp_path / "one" / "BTCUSD" / "w1", close, fc, np.zeros(n))
    write_window(tmp_path / "two" / "BTCUSD" / "w1", close, fc, np.zeros(n))
    write_window(tmp_path / "two" / "ETHUSD" / "w1", close, fc, np.zeros(n))
    one, two = size(tmp_path / "one", H), size(tmp_path / "two", H)
    assert one["unusual_move_t"] > 5 and one["case_days"] <= one["cases"]
    assert two["cases"] == 2 * one["cases"]
    assert two["unusual_move_t"] == pytest.approx(one["unusual_move_t"], rel=0.05)   # the same days: not twice as sure
