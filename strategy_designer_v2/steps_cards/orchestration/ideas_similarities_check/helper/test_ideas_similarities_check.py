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
