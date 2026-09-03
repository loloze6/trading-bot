"""
CUL-255 (c): the aux-feed resample step in DataManager._premerge_aux_feeds()
must bucket on the SAME reference point CandleBuilder._align() floors
candles against (Unix epoch, via integer division) -- not pandas' resample
default ('start_day', anchored to the midnight of the FEED'S OWN first
timestamp).

For every standard timeframe (one that evenly divides a day: 1m..1d) the two
schemes happen to agree, which is why this was invisible until CUL-250's
fetch_interval_seconds review. For a timeframe that does NOT evenly divide a
day (e.g. 7h), they silently diverge: two aux feeds starting on different
calendar days resample to DIFFERENT epoch-relative phase offsets under
pandas' default (verified directly with pandas: 23:00 vs 21:00 bucket starts
for two 7h-bucketed feeds starting three days apart -- see the epoch-phase
arithmetic below), while the price candle grid stays phase-locked to epoch
regardless of when its own data happens to start. That divergence would
silently misalign an aux bucket against the candle bar it is meant to
attach to. Fixed by passing origin="epoch" to the resample call
(data_manager.py's _premerge_aux_feeds).

_enrichment_data's own timestamps are the PRICE rows' timestamps (the
resample->merge_asof pipeline re-indexes onto them), not the resample
bucket boundaries themselves -- so this file verifies the fix directly at
its source (the resample() call actually receives origin="epoch") rather
than trying to infer bucket boundaries indirectly through the merged
output, which would conflate two different re-indexing steps.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import DataManager  # noqa: E402

SYMBOL = "BTCUSDT"


class _StubFetcher:
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.exchange_id = "binance"

    def get_data(self, symbol=None):
        return self._df

    def cache_key(self, symbol):
        return "stub"


def _hourly_price(n: int) -> pd.DataFrame:
    ts = pd.date_range("2024-03-05 03:00:00", periods=n, freq="1h")
    return pd.DataFrame({
        "timestamp": ts,
        "open": [100.0] * n, "high": [100.0] * n, "low": [100.0] * n,
        "close": [100.0] * n, "volume": [1.0] * n,
    })


def test_premerge_resample_call_uses_epoch_origin(monkeypatch):
    """Direct verification the fix is actually in place: capture the kwargs
    every DataFrame.resample() call receives during _premerge_aux_feeds and
    assert origin="epoch" was passed for the aux-feed bucketing resample."""
    n = 8
    price = _hourly_price(n)
    aux = pd.DataFrame({
        "timestamp": pd.date_range("2024-03-05 03:00:00", periods=n, freq="1h"),
        "aux_val": range(n),
    })

    captured_kwargs = []
    real_resample = pd.DataFrame.resample

    def _spy_resample(self, rule, *args, **kwargs):
        captured_kwargs.append(kwargs)
        return real_resample(self, rule, *args, **kwargs)

    monkeypatch.setattr(pd.DataFrame, "resample", _spy_resample)

    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=4 * 3600, mode="backtest", fetch_interval_seconds=3600,
    )
    dm.register_feed(name="aux_val", fetcher=_StubFetcher(aux), window_seconds=0, agg="last")
    dm.historical_data[SYMBOL] = price
    dm.initialize()

    assert captured_kwargs, "resample() was never called -- test setup didn't exercise the aux-merge path"
    assert any(kw.get("origin") == "epoch" for kw in captured_kwargs), (
        f"no resample() call in _premerge_aux_feeds passed origin='epoch' -- got calls with kwargs {captured_kwargs}"
    )


def test_epoch_origin_keeps_two_feeds_on_different_calendar_days_phase_locked():
    """Direct pandas-level proof of WHY the fix matters, independent of
    DataManager: resample a 7h-bucketed (non-day-dividing) series starting
    on two different calendar days, with and without origin='epoch'.
    Without it, the two feeds' bucket boundaries land on different
    epoch-relative phases; with it, they agree."""
    interval = "25200s"  # 7h -- does not evenly divide 86400s (1 day)

    def _first_bucket_phase(start_date: str, origin) -> int:
        s = pd.DataFrame({
            "timestamp": pd.date_range(start_date, periods=10, freq="1h"),
            "v": range(10),
        })
        kwargs = {} if origin is None else {"origin": origin}
        r = s.set_index("timestamp").resample(interval, **kwargs).agg({"v": "last"}).reset_index()
        return int(r["timestamp"].iloc[0].timestamp()) % (7 * 3600)

    default_phase_a = _first_bucket_phase("2024-03-05 03:00:00", origin=None)
    default_phase_b = _first_bucket_phase("2024-03-08 03:00:00", origin=None)
    assert default_phase_a != default_phase_b, (
        "expected pandas' default origin to phase-drift between feeds starting on "
        "different calendar days for a non-day-dividing interval -- if this now "
        "holds, the premise motivating the origin='epoch' fix no longer applies "
        "and this test (not the fix) needs revisiting"
    )

    epoch_phase_a = _first_bucket_phase("2024-03-05 03:00:00", origin="epoch")
    epoch_phase_b = _first_bucket_phase("2024-03-08 03:00:00", origin="epoch")
    assert epoch_phase_a == epoch_phase_b == 0, (
        f"origin='epoch' must phase-lock both feeds to the same epoch-relative "
        f"boundary regardless of start date -- got {epoch_phase_a} and {epoch_phase_b}"
    )


def test_epoch_origin_is_a_no_op_for_a_standard_day_dividing_timeframe():
    """Byte-identity/no-regression proof: for 4h (evenly divides a day, the
    only kind of interval actually used in this codebase today), origin='epoch'
    and pandas' default produce IDENTICAL bucket boundaries."""
    s = pd.DataFrame({
        "timestamp": pd.date_range("2024-03-05 03:17:00", periods=20, freq="37min"),
        "v": range(20),
    })
    default = s.set_index("timestamp").resample("14400s").agg({"v": "last"}).reset_index()
    epoch = s.set_index("timestamp").resample("14400s", origin="epoch").agg({"v": "last"}).reset_index()
    assert list(default["timestamp"]) == list(epoch["timestamp"])
    assert list(default["v"]) == list(epoch["v"])
