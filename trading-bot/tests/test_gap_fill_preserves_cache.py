"""
Optional gap-fill must not discard cached data that already covers the window
(CUL-230, 2026-09-02).

Defect: `_identify_missing_periods` schedules a live top-up for any hole in the
requested window. When that top-up fails — a raising `_fetch_remote` (network /
rate limit), or a `FetchGapError` from `_merge_and_store` refusing a
non-connecting response — the exception propagated out of `_load_all`/`get_data`
and `fetch_historical_data`'s blanket handler degraded it to an empty frame,
which `launcher.py` then reported as `RuntimeError: No historical data`. An 8-year
cache that fully covered the window was thrown away because a 4-hour internal
hole could not be topped up.

Fix: the read-only backtest path opts in (`tolerate_fill_failure=True`, set by
`DataManager.fetch_historical_data`) to fall back to the cached rows — BUT only
when, bounded to the requested window, the cache reaches both boundaries within
one interval. Interior holes (the real CUL-230 case) are tolerated; a boundary
shortfall re-raises (returning a short window would silently backtest a different
range than asked — launcher.py rejects only EMPTY frames). Three further
exclusions always fail loud: `SealedDataError`, an empty in-window cache, and —
flag OFF by default — the write/append callers (capture tools depend on a
non-connecting fetch still raising).

Fixtures only — no live calls. `_fetch_remote` is stubbed per test.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import data.fetchers.ccxt_fetcher as ccxt_fetcher  # noqa: E402
from data.data_manager import DataManager, SealedDataError  # noqa: E402
from data.fetchers.base_fetcher import BaseFetcher, FetchGapError  # noqa: E402

HOUR = 3600


def _bars(start: str, periods: int) -> pd.DataFrame:
    """OHLCV-shaped frame; only `timestamp` drives gap detection."""
    ts = pd.date_range(start=start, periods=periods, freq="1h")
    return pd.DataFrame({
        "timestamp": ts,
        "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0,
    })


def _cache_with_interior_gap() -> pd.DataFrame:
    """44 hourly bars spanning the FULL 2020-06-01..2020-06-02 window (reaches
    both boundaries: 06-01 00:00 and 06-02 23:00) with one 5h interior hole
    (drops 10:00..13:00 on 06-01). This is the CUL-230 shape — tolerated."""
    return pd.concat(
        [_bars("2020-06-01 00:00", 10), _bars("2020-06-01 14:00", 34)],
        ignore_index=True,
    )


class _CacheFetcher(BaseFetcher):
    """Concrete BaseFetcher whose `_fetch_remote` is injected per test."""

    def __init__(self, tmp_dir, start, end, remote, tolerate=True):
        self._remote = remote
        super().__init__(
            start_date=start, end_date=end, symbols=["BTCUSD"],
            interval_seconds=HOUR, localStorage=True, data_dir=str(tmp_dir),
        )
        self.tolerate_fill_failure = tolerate

    def _fetch_remote(self, symbol, start, end):
        return self._remote(symbol, start, end)

    def cache_key(self, symbol):
        return symbol


def _write_cache(tmp_dir, symbol, df):
    df.to_csv(Path(tmp_dir) / f"{symbol}.csv", index=False)


def _raise(exc):
    def _remote(symbol, start, end):
        raise exc
    return _remote


# ---------------------------------------------------------------------------
# Interior hole + failed fill (tolerate=True) -> the FULL window is kept
# ---------------------------------------------------------------------------

def test_interior_gap_kept_on_raising_fetch(tmp_path):
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    got = f.get_data("BTCUSD")

    assert len(got) == 44
    # the returned window spans the full request, not a truncation
    assert got["timestamp"].min() == pd.Timestamp("2020-06-01 00:00")
    assert got["timestamp"].max() == pd.Timestamp("2020-06-02 23:00")


def test_interior_gap_kept_on_fetchgaperror(tmp_path):
    """A FetchGapError originating in the merge (its natural source) is caught
    and, because the cache reaches both boundaries, the full window is kept —
    NOT truncated to whatever partial the fetch returned."""
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())

    def empty_fill(symbol, start, end):
        return pd.DataFrame()

    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02", empty_fill)

    # force the write-guard to reject the merge, as a non-connecting live
    # response would (the naturally interior gap cannot itself trigger it).
    def reject_merge(*args, **kwargs):
        raise FetchGapError("non-connecting response")

    f._merge_and_store = reject_merge

    got = f.get_data("BTCUSD")
    assert len(got) == 44
    assert got["timestamp"].min() == pd.Timestamp("2020-06-01 00:00")
    assert got["timestamp"].max() == pd.Timestamp("2020-06-02 23:00")


# ---------------------------------------------------------------------------
# Boundary shortfall -> the failure still surfaces (no silent short window)
# ---------------------------------------------------------------------------

def test_boundary_missing_at_start_reraises(tmp_path):
    """Cache begins 5h INTO the window (missing 00:00..04:00). Falling back
    would backtest 06-01 05:00.. as if it were the requested 06-01 00:00.. —
    the failure must surface instead."""
    _write_cache(tmp_path, "BTCUSD", _bars("2020-06-01 05:00", 43))  # -> 06-02 23:00
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


def test_boundary_missing_at_end_reraises(tmp_path):
    """Cache ends 4h BEFORE the window end (missing 20:00..23:00 on 06-02)."""
    _write_cache(tmp_path, "BTCUSD", _bars("2020-06-01 00:00", 44))  # -> 06-02 19:00
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


def test_missing_leading_bar_reraises(tmp_path):
    """One whole missing bar at the window start (cache begins 06-01 01:00 for a
    00:00 request, on-grid) is a boundary shortfall, not off-grid slack — strict
    `<` re-raises rather than silently backtesting from 01:00."""
    _write_cache(tmp_path, "BTCUSD", _bars("2020-06-01 01:00", 47))  # -> 06-02 23:00
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


def test_off_grid_start_within_first_interval_kept(tmp_path):
    """An off-grid request (12:30 on a 1h grid) whose first cached bar (13:00)
    sits inside the first interval is genuine coverage — strict `<` keeps it."""
    _write_cache(tmp_path, "BTCUSD", _bars("2020-06-01 13:00", 35))  # -> 06-02 23:00
    f = _CacheFetcher(tmp_path, "2020-06-01 12:30", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    got = f.get_data("BTCUSD")

    assert len(got) == 35
    assert got["timestamp"].min() == pd.Timestamp("2020-06-01 13:00")
    assert got["timestamp"].max() == pd.Timestamp("2020-06-02 23:00")


def test_no_cached_rows_failure_still_surfaces(tmp_path):
    # no cache file on disk -> existing is empty -> nothing to fall back to
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


def test_seal_guard_from_fetch_still_propagates(tmp_path):
    """A seal guard must fail loud even when the cache covers the window and the
    flag is on — holdout safety is never downgraded to a warning fallback."""
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(SealedDataError("holdout window touched")))
    with pytest.raises(SealedDataError):
        f.get_data("BTCUSD")


# ---------------------------------------------------------------------------
# Flag OFF (default) -> even a coverable interior gap fails loud (capture path)
# ---------------------------------------------------------------------------

def test_default_is_strict_reraises(tmp_path):
    """With the flag OFF (default, used by the capture tools), a failed fill
    re-raises even when the cache covers the window — the read-path leniency
    must never leak into write/append callers."""
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")),
                      tolerate=False)
    assert f.tolerate_fill_failure is False
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


# ---------------------------------------------------------------------------
# A successful fill still fills and writes (no regression on the happy path)
# ---------------------------------------------------------------------------

def test_successful_fill_still_merges(tmp_path):
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())

    def remote(symbol, start, end):
        return _bars("2020-06-01 10:00", 4)           # exactly the 5h hole's bars

    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02", remote)
    got = f.get_data("BTCUSD")

    assert len(got) == 48                             # 44 cached + 4 filled
    assert pd.Timestamp("2020-06-01 11:00") in set(got["timestamp"])
    assert len(pd.read_csv(Path(tmp_path) / "BTCUSD.csv")) == 48


# ---------------------------------------------------------------------------
# End-to-end: fetch_historical_data wires the read-path leniency (the CUL-230 bug)
# ---------------------------------------------------------------------------

def test_fetch_historical_data_returns_window_when_gap_fill_raises(tmp_path, monkeypatch):
    """The literal crash path: an interior-gap cache + a raising fill must return
    the full cached window through DataManager.fetch_historical_data, not the
    empty frame that launcher.py turns into 'No historical data'."""
    # CcxtFetcher (exchange=binance) resolves the cache slot to "<symbol>_<tf>".
    _write_cache(tmp_path, "BTCUSD_1h", _cache_with_interior_gap())

    orig_init = ccxt_fetcher.CcxtFetcher.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["data_dir"] = str(tmp_path)
        orig_init(self, *args, **kwargs)
        self.exchange = None

    monkeypatch.setattr(ccxt_fetcher.CcxtFetcher, "__init__", patched_init)
    monkeypatch.setattr(
        ccxt_fetcher.CcxtFetcher, "_fetch_remote",
        lambda self, symbol, start, end: (_ for _ in ()).throw(RuntimeError("network down")),
    )

    manager = DataManager(["BTCUSD"], interval_seconds=HOUR, mode="backtest")
    df = manager.fetch_historical_data("BTCUSD", "2020-06-01", "2020-06-02")

    assert len(df) == 44
    assert df["timestamp"].min() == pd.Timestamp("2020-06-01 00:00")
    assert df["timestamp"].max() == pd.Timestamp("2020-06-02 23:00")
