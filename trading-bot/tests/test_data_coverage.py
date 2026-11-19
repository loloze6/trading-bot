"""Data gathering separate from the backtest (operator 2026-11-18): the coverage record (data/coverage.py), the
backtest loader that reads local files only (BaseFetcher.remote False), and the fetch that records what it stored."""
import datetime as dt
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data import coverage  # noqa: E402
from data.coverage import DataNotFetched  # noqa: E402
from data.fetchers.base_fetcher import BaseFetcher  # noqa: E402

D = dt.date


def test_ranges_merge_and_missing_days(tmp_path):
    coverage.record(tmp_path, "f.csv", "2023-01-01", "2023-12-31", "a")
    coverage.record(tmp_path, "f.csv", "2025-01-01", "2025-06-30", "b")
    assert coverage.missing(tmp_path, "f.csv", "2023-06-01", "2023-12-31 23:59:59") == []
    assert coverage.missing(tmp_path, "f.csv", "2023-06-01", "2025-02-01") == [(D(2024, 1, 1), D(2024, 12, 31))]
    coverage.record(tmp_path, "f.csv", "2024-01-01", "2024-12-31", "c")             # the hole fetched: one range
    assert coverage.ranges(coverage.load(tmp_path)["f.csv"]) == [(D(2023, 1, 1), D(2025, 6, 30))]
    assert coverage.missing(tmp_path, "f.csv", "2022-12-30", "2025-07-02") == [(D(2022, 12, 30), D(2022, 12, 31)),
                                                                               (D(2025, 7, 1), D(2025, 7, 2))]
    assert coverage.missing(tmp_path, "other.csv", "2023-01-01", "2023-01-02") == [(D(2023, 1, 1), D(2023, 1, 2))]


def test_a_null_start_covers_everything_before(tmp_path):
    coverage.record(tmp_path, "k.csv", None, "2025-12-31", "the pair's whole history")
    assert coverage.missing(tmp_path, "k.csv", "2010-01-01", "2025-12-31") == []
    assert coverage.missing(tmp_path, "k.csv", "2010-01-01", "2026-01-02") == [(D(2026, 1, 1), D(2026, 1, 2))]
    with pytest.raises(DataNotFetched, match="2026-01-01 to 2026-01-02 not fetched"):
        coverage.check(tmp_path, "k.csv", "2025-12-01", "2026-01-02")


class Fake(BaseFetcher):
    """A fetcher whose exchange answers from a given frame, and records each call."""
    answer = pd.DataFrame()

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.calls = []

    def cache_key(self, symbol):
        return f"{symbol}_1h"

    def _fetch_remote(self, symbol, start, end):
        self.calls.append((start, end))
        return self.answer


def hourly(start, hours, skip=()):
    ts = [t for i, t in enumerate(pd.date_range(start, periods=hours, freq="h")) if i not in skip]
    return pd.DataFrame({"timestamp": ts, "close": range(len(ts))})


def test_the_backtest_loader_reads_the_file_only(tmp_path):
    hourly("2023-01-01", 24 * 10, skip=(30, 31, 32)).to_csv(tmp_path / "X_1h.csv", index=False)  # a 3-hour hole
    coverage.record(tmp_path, "X_1h.csv", None, "2023-01-10", "test")
    f = Fake("2023-01-02", "2023-01-05", ["X"], 3600, True, str(tmp_path))
    f.remote = False
    got = f.get_data("X")
    assert f.calls == []                                   # the hole is read as it is: no call
    assert len(got) == 4 * 24 - 3
    f = Fake("2023-01-09", "2023-01-12", ["X"], 3600, True, str(tmp_path))
    f.remote = False
    with pytest.raises(DataNotFetched, match="2023-01-11 to 2023-01-12"):
        f.get_data("X")
    assert f.calls == []


def test_a_saved_fetch_records_what_the_exchange_returned(tmp_path):
    hourly("2023-01-01", 24 * 2).to_csv(tmp_path / "X_1h.csv", index=False)
    Fake.answer = hourly("2023-01-03", 24 * 2)
    f = Fake("2023-01-01", "2023-01-04", ["X"], 3600, True, str(tmp_path))
    f.get_data("X")
    assert f.calls                                         # the default (a data tool) still fetches
    assert coverage.ranges(coverage.load(tmp_path)["X_1h.csv"]) == [(D(2023, 1, 3), D(2023, 1, 4))]
    Fake.answer = pd.DataFrame()


def test_the_backtest_loader_lets_the_refusal_through(monkeypatch):
    import data.data_manager as dm

    class Refusing:
        tolerate_fill_failure = False

        def __init__(self, *a, **k):
            pass

        def get_data(self):
            raise DataNotFetched("X_1h.csv: 2024-01-01 to 2024-12-31 not fetched")

    monkeypatch.setattr(dm, "HistoricalDataFetcher", Refusing)
    mgr = dm.DataManager.__new__(dm.DataManager)
    mgr.interval_seconds = 3600
    mgr.fetch_interval_seconds = 3600
    with pytest.raises(DataNotFetched):                    # not degraded to an empty frame ("no data")
        dm.DataManager.fetch_historical_data(mgr, "BTCUSD", "2022-01-01", "2022-02-01", exchange="kraken")


def test_the_data_bar_is_the_largest_file_bar_that_divides_the_trading_bar(tmp_path):
    for f in ("kraken_X_1d.csv", "kraken_X_1h.csv", "kraken_Y_1h.csv", "X_1h.csv"):
        coverage.record(tmp_path, f, None, "2025-12-31", "test")
    assert coverage.data_bar(tmp_path, "kraken_X", 86400) is None          # 1d has its own file: read as it is
    assert coverage.data_bar(tmp_path, "kraken_X", 3600) is None           # 1h too
    assert coverage.data_bar(tmp_path, "kraken_X", 4 * 3600) == 3600       # 4h is built from 1h
    assert coverage.data_bar(tmp_path, "kraken_X", 2 * 86400) == 86400     # 2d from 1d
    assert coverage.data_bar(tmp_path, "kraken_Y", 12 * 3600) == 3600
    assert coverage.data_bar(tmp_path, "kraken_X", 1800) is None           # nothing finer than 30m: no file fits
    assert coverage.data_bar(tmp_path, "kraken_Z", 4 * 3600) is None       # no file for the coin
